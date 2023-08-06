# coding: utf-8
from abc import ABCMeta, abstractmethod
from pydoc import locate
from .exceptions import NotApplicableException, RuleConfigurationException
from .model import DialMarcXMLObject, DialObject

import logging
import libxml2
import json
import os
import re
import pkg_resources

from pprint import pprint


logger = logging.getLogger(__name__)


SUCCESS = 10
FAILED = 0


class DialObjectChecker(object):

    def __init__(self, rules_directory=None):
        self.rules = []

        if not rules_directory:
            resource_package = __name__  # Could be any module/package name
            resource_path = 'rules'  # Do not use os.path.join()
            rules_directory = pkg_resources.resource_filename(resource_package, resource_path)

        for file_name in [file_name for file_name in os.listdir(rules_directory) if file_name.endswith('.json')]:
            with open(os.path.join(rules_directory, file_name), 'r') as fh:
                rules = json.load(fh)
                if not isinstance(rules, list):
                    rules = [rules]
                for rule_config in rules:
                    self.rules.append(DialValidationRule.builder(rule_config))

    def check_object(self, fc_obj):
        """
            This function check a FedoraCommons object from DIAL with all the rules loaded for this checker.
            Before using a validation rule, the rule condition are checked to know if the rule must be validated or not.
            If all rules condition are reached, then the function try to validate the rule.
            This function return all the used rule and for each rule, the validation status (SUCCES or FAILED).

            :param fc_obj: the FedoraCommons object to check
            :type fc_obj: :class:'eulfedora.models.DigitalObject'
            :return: return a list of tuples. Each tuple contains 2 values:
                        * first value will be the rule status (pydial.checker.SUCCESS or pydial.checker.FAILED)
                        * second : the rule checked (:class:'DialValidationRule' subclass)
            :rtype: a list of tuples
        """
        # First we need to get all applicable rules for this object depending of conditions defined for each rules.
        # 'applicable_rule' is a list of tuples. Each tuple have 2 values :
        #    - the rule status (SUCCESS|FAILED). By default we place all rules to SUCCESS
        #    - the rule to check as :class:'DialValidationRule' subclass
        applicable_rules = filter(lambda r: r.check_conditions(fc_obj), self.rules)
        applicable_rules = [(SUCCESS, rule) for rule in applicable_rules]
        logger.debug("Number of rules to applied to validate this object : {len}".format(len=len(applicable_rules)))
        # Now iterate each applicable rules. If rule validation failed, we need to update the corresponding tuple
        # to set the rule status to FAILED.
        for idx, rule in enumerate(applicable_rules):
            check_result = rule[1].check(fc_obj)
            logger.debug("  * testing rule [{rule}] {filler} {status}".format(
                rule=rule[1].name,
                filler="." * (55-len(rule[1].name)),
                status='SUCCESS' if check_result else 'FAILED'
            ))
            if not check_result:  # rule validation failed, need to change the tuple
                applicable_rules[idx] = tuple([FAILED, rule[1]])
        # return the list of applicable rules. To filter only on FAILED rules use :
        # >>> rules = DialObjectChecker.filter_rules(rules_list, DialObjectChecker.FAILED)
        return applicable_rules

    @staticmethod
    def filter_rules(rules, status=SUCCESS):
        filtered_rules = filter(lambda r: r[0] == status, rules)
        return [rule for status, rule in filtered_rules]


# ======================================================================================================================
#    CONDITION RULE
# ======================================================================================================================
class DialValidationRule(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.config = kwargs
        DialValidationRule.check_required_params(['name', 'description', 'level', 'class'], self.config)
        self.level = logging.getLevelName(kwargs['level'])
        if not isinstance(self.level, int):
            raise ValueError("'{level}' isn't a valid value :: [CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG]".format(
                level=kwargs['level']
            ))
        self.conditions = []
        if 'conditions' in kwargs:
            for condition_config in kwargs['conditions']:
                self.conditions.append(ConditionRule.builder(condition_config))
        if 'params' in kwargs:
            if not isinstance(kwargs['params'], dict) or len(kwargs['params']) < 1:
                raise TypeError("'params' param must be a dict")
        else:
            self.params = {}

    @staticmethod
    def check_required_params(required_params, data):
        if not all(k in data for k in required_params):
            raise RuleConfigurationException("missing required params :: "+str(required_params))

    @staticmethod
    def builder(config):
        cls = locate(config['class'])
        if cls is None:
            raise NameError("the {class_name} class cannot be found".format(class_name=config['class']))
        else:
            return cls(**config)

    def __getattr__(self, item):
        if item in self.config:
            return self.config[item]
        return None

    def check_conditions(self, fc_obj):
        for condition in self.conditions:
            try:
                condition.check(fc_obj)
            except NotApplicableException as nae:
                logger.debug(str(nae))
                return False
        return True

    @abstractmethod
    def check(self, fc_obj):
        raise NotImplementedError


class DatastreamValidationRule(DialValidationRule):

    def __init__(self, **kwargs):
        super(DatastreamValidationRule, self).__init__(**kwargs)
        DialValidationRule.check_required_params(['params'], self.config)
        DialValidationRule.check_required_params(['datastreams'], self.params)

        if isinstance(self.params['datastreams'], basestring):
            self.required_datastreams = [self.required_datastreams]
        if not isinstance(self.params['datastreams'], list) \
                or not all(isinstance(ds, basestring) for ds in self.params['datastreams']) \
                or len(self.params['datastreams']) < 1:
            raise TypeError("'datastreams' parameter must be a list of string")

    def check(self, fc_obj):
        missing_ds = [ds_id for ds_id in self.params['datastreams'] if ds_id not in fc_obj.ds_list]
        return len(missing_ds) == 0


class XPathValidationRule(DialValidationRule):

    def __init__(self, **kwargs):
        super(XPathValidationRule, self).__init__(**kwargs)
        DialValidationRule.check_required_params(['params'], self.config)
        DialValidationRule.check_required_params(['datastream', 'xpath'], self.params)
        if 'namespaces' not in self.params:
            self.params['namespaces'] = {}

    def check(self, fc_obj):
        if self.params['datastream'] not in fc_obj.ds_list:
            return False
        try:
            datastream = fc_obj.getDatastreamObject(self.params['datastream'])
            xml = libxml2.parseDoc(datastream.content.serializeDocument())
            context = xml.xpathNewContext()
            for name, uri in self.params['namespaces'].items():
                context.xpathRegisterNs(name, uri)
            tags = context.xpathEval(self.params['xpath'])
            tags = [tag.content.decode('utf-8') for tag in tags]
            xml.freeDoc()
            context.xpathFreeContext()
            # If rule 'regexp' is defined, check all found values with this regexp. If one failed, return False
            # If no 'regexp' are defined for this rule, then just check than xpath found one or more values
            if 'regexp' in self.params:
                if 'any' in self.params and self.params['any'] is True:
                    return any(re.match(self.params['regexp'], tag) for tag in tags)
                else:
                    return all(re.match(self.params['regexp'], tag) for tag in tags)
            else:
                return len(tags) > 0
        except Exception as e:
            logger.exception(e)
            return False


class FWBOAValidationRule(DialValidationRule):
    """
        Using this validation rule, you can check if a FedoraCommons object is valid relative to FWB OpenAccess decree.
        To be valid, any scientific publication need to provide at least one fulltext in OpenAccess or embargo access
        limited ini the time (12 or 6 months depending of research sector)
    """

    def check(self, fc_obj):
        if not issubclass(fc_obj.__class__, DialObject):
            fc_obj = DialObject(fc_obj.api, fc_obj.pid)  # reload the object as a DialObject
        files = fc_obj.attached_files
        valid_files = [f for ds_id, f in files.items() if f.access_type in ['OpenAccess', 'embargo']]
        return valid_files  # if valid_files is empty, return False


# ======================================================================================================================
#    CONDITION RULE
# ======================================================================================================================
class ConditionRule(object):
    """
        A condition rule is used to determine if a :class:'DialValidationRule' could be tested for a specific
        FedoraCommons object. This class is an abstract class, and only subclasses must be used. Each subclass need to
        implement the :method:'self.check(fc_obj)' to determine if the ConditionRule is valid or not.

        requested arguments:
            - 'class': the full class name of the condition. This class must be a subclass of :class:'ConditionRule'.
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.params = kwargs
        self._check_required_params(['class'])

    def __getattr__(self, item):
        return self.params[item]

    def _check_required_params(self, required_params):
        if not all(k in self.params for k in required_params):
            raise RuleConfigurationException("missing required params :: "+str(required_params))

    @staticmethod
    def builder(config):
        """ This static function must be used to create an instance of :class:'ConditionRule' subclass depending of
            the configuration. Configuration must be a dict of params used to build the rule with at least the 'class'
            key representing the full :class:'ConditionRule' subclass name

            :param config: the configuration af the rule. Each configuration depend of the rule. See specific class rule
                           documentation to know the requested parameters.
            :type config: dict
            :return: A :class:'ConditionRule' subclass instance corresponding to 'class' param
            :rtype: :class:'ConditionRule' subclass instance

            :raise: NameError: if the :class:'ConditionRule' subclass cannot be found
            :raise: RuleConfigurationException: if some params are missing for about the rule
        """
        if 'class' not in config:
            raise RuleConfigurationException("Missing 'class' parameter for ConditionRule :: "+str(config))
        cls = locate(config['class'])
        if cls is None:
            raise NameError("the {class_name} class cannot be found".format(class_name=config['class']))
        else:
            return cls(**config)

    @abstractmethod
    def check(self, fc_obj):
        raise NotImplementedError


class ContentModelConditionRule(ConditionRule):
    """
        Using this class, we can check if a validation rule is applicable depending of a FedoraCommons object content
        models. If the object has the correct content model, then the condition is reached ; otherwise, the condition
        isn't applicable and the validation rule should be skipped.

        requested arguments:
            - 'values': a list of allowed "content-model" values. If one of them are found for the object, then the
                        condition is valid.
    """

    def __init__(self, **kwargs):
        super(ContentModelConditionRule, self).__init__(**kwargs)
        self._check_required_params(['values'])
        if not isinstance(self.values, list) \
                or not all(isinstance(v, basestring) for v in self.values) \
                or len(self.values) < 1:
            raise TypeError("'values' param must be a list of string")

    def check(self, fc_obj):
        for content_model in self.values:
            if fc_obj.has_model(content_model):
                return
        raise NotApplicableException(origin=self.__class__.__name__, fc_obj=fc_obj)


class StateConditionRule(ConditionRule):
    """
        Using this class, we can check if a validation rule is applicable depending of the FedoraCommons object state.
        If the state of the object are listed into allowed values, then the condition is reached ; otherwise, the
        condition isn't applicable and the validation rule should be skipped.

        requested arguments:
            - 'values': a list of allowed state values ('A' for Active, 'I' for Inactive, 'D' for deleted).
    """

    def __init__(self, **kwargs):
        super(StateConditionRule, self).__init__(**kwargs)
        self._check_required_params(['values'])
        if not isinstance(self.values, list) \
                or not all(isinstance(v, basestring) for v in self.values) \
                or len(self.values) < 1:
            raise TypeError("'values' param must be a list of string")

    def check(self, fc_obj):
        if fc_obj.state not in self.values:
            raise NotApplicableException(
                origin=self.__class__.__name__,
                fc_obj=fc_obj,
                message="""state is "{s}" """.format(s=fc_obj.state)
            )


class XPathConditionRule(ConditionRule):
    """
        Using this class, we can check if a validation rule is applicable depending of the an xpath execution success
        on a datastream of the object. If the Xpath check return one or more values, then the condition is reached.
        If datastream is not a valid XML datastream, then the condition isn't applicable.
        If the xpath execution return non values, then the condition isn't applicable and the validation rule should
        be skipped.

        requested arguments:
            - 'datastream': the ID of the datastream where to execute the xpath
            - 'xpath': the xpath to find
            - 'namespaces': a dictionary of namespaces used by the xpath (optional)
    """

    def __init__(self, **kwargs):
        super(XPathConditionRule, self).__init__(**kwargs)
        self._check_required_params(['datastream', 'xpath'])
        if 'namespaces' not in kwargs:
            self.namespaces = {}

    def check(self, fc_obj):
        if self.datastream not in fc_obj.ds_list:
            raise NotApplicableException(
                origin=self.__class__.__name__,
                fc_obj=fc_obj,
                message="Datastream {ds_id} not available".format(ds_id=self.datastream)
            )
        try:
            datastream = fc_obj.getDatastreamObject(self.datastream)
            xml = libxml2.parseDoc(datastream.content.serialize())
            context = xml.xpathNewContext()
            for name, uri in self.namespaces.items():
                context.xpathRegisterNs(name, uri)
            tags = context.xpathEval(self.xpath)
            tags = len(tags)
            xml.freeDoc()
            context.xpathFreeContext()
            if tags < 1:
                raise NotApplicableException(
                    origin=self.__class__.__name__,
                    fc_obj=fc_obj,
                    message="xpath {x} doesn't return anything".format(x=self.xpath)
                )
        except Exception as e:
            raise e


class IsScientificArticleConditionRule(ConditionRule):
    """
        This condition will check if the FedoraCommons object is a 'scientific article' relative to DIAL defined rules.
        This condition should be used to filter object valid for FWB OA decree.
        To be considerate as 'scientific article', the publication must be :
          - either a 'serial article' either a 'conference speech'
          - for article : not a 'article de vulgarisation' or 'numéro entier'
          - for speech: published either in a serial, either in a book

        !!! to be eligible for FWB OA decree, this condition must be coupled with an XPathConditionRule to test the
            publication year (>2018)
    """

    def check(self, fc_obj):
        document_type = None
        if fc_obj.has_model("info:fedora/boreal-system:ArticleCM"):
            document_type = "info:fedora/boreal-system:ArticleCM"
        elif fc_obj.has_model("info:fedora/boreal-system:SpeechCM"):
            document_type = "info:fedora/boreal-system:SpeechCM"

        # [1] check object is a 'serial' or a 'speech'
        if document_type is None:
            raise NotApplicableException(
                origin=self.__class__.__name__,
                fc_obj=fc_obj,
                message="[{pid}] content model mismatch".format(pid=fc_obj.pid)
            )
        # [2] reload the object as a DialMarcxml object, so we can use the custom function (get_metadata, ...)
        fc_obj = DialMarcXMLObject(fc_obj.api, fc_obj.pid)

        # [3] Article check
        if document_type == 'info:fedora/boreal-system:ArticleCM':
            document_subtype = fc_obj.get_metadata('955', 'b')
            if document_subtype in [u'Article de vulgarisation', u'Numéro entier']:
                raise NotApplicableException(
                    origin=self.__class__.__name__,
                    fc_obj=fc_obj,
                    message="document subtype mismatch"
                )
            publication_status = fc_obj.get_metadata('973', 'a')
            if publication_status == u'Soumis':
                raise NotApplicableException(
                    origin=self.__class__.__name__,
                    fc_obj=fc_obj,
                    message="publication status mismatch"
                )
        # [3] Speech check
        if document_type == 'info:fedora/boreal-system:SpeechCM':
            if len(fc_obj.get_fields('779')) > 0:
                # published in a book !
                return
            if fc_obj.get_metadata('773', 't') is not None:
                # published in a serial. Sometimes 773 field is present only for 'peer-reviewed' tag but the speech
                # is not published
                return
            raise NotApplicableException(
                origin=self.__class__.__name__,
                fc_obj=fc_obj,
                message="Not published"
            )
