from pymarc import Record, Field
import pymarc.marcxml as marcxml
from .exceptions import MappingException
import model
import json
import os
import re
import lxml.etree as ET


class PublicationRecordBuilder(object):
    """
        The purpose of this class is to transform JSON data into MARC record.

        Using the json schemas, we can validate the JSON data that we received ; After the validation process, we need
        to transform these JSON data into a MARC record used by DIAL.pr (for MARCXML datastream).
        As the MARCXML datastream should be different depending of the documentType version, some class should inherit
        from :class:PublicationBuilder to extends the MARC record with specific metadata.

        attributes:
            * mappings : A dict of all maps used to translate some JSON value to expected MARCXML metadata. These maps
                         are loaded from the configuration file 'mappings.json' located in the 'conf' directory from the
                         current filepath.
    """

    NOT_APPLICABLE = ['na', 'NA', 'n/a', 'N/A', 'not applicable']

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'conf/mapping.json')) as fh:
            self.mappings = json.load(fh)

    def _get_basic_record(self, data):
        record = Record()
        record.force_utf8 = True
        self._add_basic_tags(record, data)
        return record

    def _apply_mapping(self, mapping_type, value, ignore_error=False):
        """
            This function apply a mapping for a specific value. The maps are loaded from a configuration file (see
            self.mappings). If 'ignore_error' are True, no exception will be raise if the map between value and maps
            failed ; then the 'value' will be return without transformation

            :param mapping_type: the name of the map into self.mappings dictionary
            :param value: the value to map (key of the `mapping_type` dictionary)
            :param ignore_error: if set to 'False', raise an error if mapping failed ; if set to True, no error will be
                                 raised and 'value' will be return without transformation.
            :return: the transformed value
            :rtype: string
            :raise MappingException: If the mapping failed and 'ignore_error' param are set to 'False'
        """
        if mapping_type not in self.mappings:
            if not ignore_error:
                raise MappingException("'{t}' section doesn't exists into the mapping file".format(t=mapping_type))
            return value
        if value not in self.mappings[mapping_type]:
            if not ignore_error:
                raise MappingException("'{k}' isn't a valid key for '{t}'".format(k=value, t=mapping_type))
            return value
        return self.mappings[mapping_type][value]

    def _add_basic_tags(self, record, data):
        """
            This function add basics tags than each publication can have into it (define by basic-schema JSON schema).
            Read into the function to know which datafield are created with which subfields.

            :param record: the MARC record to fill with new MARC datafield.
            :param data: the JSON data parse as a dict
        """
        # AUTHORS sections ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   100|700 ['','']  $a : name
        #                    $g : email
        #                    $5 : institution
        #                    $i : institution_id (only if 'institution' exists)
        #                    $e : role
        if 'authors' in data:
            for idx, author in enumerate(data['authors']):
                tag = '100' if idx == 0 else '700'
                subfields = []
                for code, field_name in model.DialMarcXMLObject.AUTHOR_SUBFIELD_MAP.items():
                    if field_name in author:
                        if field_name == 'role':
                            subfields.extend([code, self._apply_mapping('author_role_mapping', author[field_name])])
                        else:
                            subfields.extend([code, author[field_name]])
                record.add_ordered_field(Field(tag=tag, indicators=['', ''], subfields=subfields))

        # TITLE_INFO section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   245 ['','']  $a : title + subtitle
        #                $c : 'et al.' if additional authors exists
        if 'title_info' in data and 'title' in data['title_info']:
            subfields = []
            if 'subtitle' in data['title_info']:
                subfields.extend(['a', u' : '.join([data['title_info']['title'], data['title_info']['subtitle']])])
            else:
                subfields.extend(['a', data['title_info']['title']])
            if 'additional_authors' in data and data['additional_authors'] is True:
                subfields.extend(['c', 'et al.'])
            record.add_ordered_field(Field(tag='245', indicators=['', ''], subfields=subfields))

        # DOCUMENT_TYPE section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   955 ['','']  $a : main document type
        #                $b : subtype
        if 'type' in data:
            subfields = []
            if 'document_type' in data['type']:
                subfields.extend(['a', self._apply_mapping('document_type_mapping', data['type']['document_type'])])
            if 'document_subtype' in data['type']:
                subfields.extend(['b', data['type']['document_subtype']])
            record.add_ordered_field(Field(tag='955', indicators=['', ''], subfields=subfields))

        # ABSTRACT section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   520 ['','']  $a : abstract content
        #                $x : abstract iso code language
        if 'abstracts' in data and data['abstracts']:
            for abstract in data['abstracts']:
                subfields = ['a', abstract['content']]
                if 'language' in abstract:
                    subfields.extend(['x', abstract['language']])
                record.add_ordered_field(Field(tag='520', indicators=['', ''], subfields=subfields))

        # YEAR section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   260 ['', '']  $c : publication year
        #   !! $a (publishing place) and $b (publisher name) can be added depending of the document type
        if 'year' in data and data['year'] not in PublicationRecordBuilder.NOT_APPLICABLE:
            record.add_ordered_field(Field(tag='260', indicators=['', ''], subfields=['c', data['year']]))

        # LANGUAGE section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   041 ['', '']  $a : language iso code
        #   546 ['', '']  $a : language human readable name
        if 'language' in data:
            record.add_ordered_field(Field(tag='041', indicators=['', ''], subfields=['a', data['language']]))
            record.add_ordered_field(Field(tag='546', indicators=['', ''], subfields=[
                'a',
                self._apply_mapping('language_label_mapping', data['language'], ignore_error=True)
            ]))

        # KEYWORDS section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   699 ['', '']  $a : publication keyword
        #   698 ['', '']  $a : internal use keyword
        #   650 ['2', ''] $a : Medical Subject Heading (MESH)
        if 'keywords' in data and data['keywords']:
            for keyword in data['keywords']:
                record.add_ordered_field(Field(tag='699', indicators=['', ''], subfields=['a', keyword]))
        if 'internal_keywords' in data and data['internal_keywords']:
            for keyword in data['internal_keywords']:
                record.add_ordered_field(Field(tag='698', indicators=['', ''], subfields=['a', keyword]))
        if 'mesh_keywords' in data and data['mesh_keywords']:
            for keyword in data['mesh_keywords']:
                keyword = re.sub(r'^MESH:', '', keyword, flags=re.IGNORECASE)
                record.add_ordered_field(Field(tag='650', indicators=['2', ''], subfields=['a', keyword]))

        # URLS section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   865 ['4', '0']  $u : the full URL (except for DOI)
        #                   $z : (optional) the URL type (Pubmed, DOI, Handle, ...)
        if 'urls' in data and data['urls']:
            for url in data['urls']:
                subfields = ['u', url]
                if 'pubmed' in url:
                    subfields.extend(['z', 'Pubmed'])
                elif 'dx.doi.org' in url:
                    subfields = [
                        'u', re.sub(r'http[s]?://dx.doi.org/', '', url),
                        'z', 'DOI'
                    ]
                elif 'hdl.handle.net' in url:
                    subfields.extend(['z', 'Handle'])
                record.add_ordered_field(Field(tag='856', indicators=['4', '0'], subfields=subfields))

        # ENTITIES section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   988 ['', '']  $a : institution name (owner of the entity)
        #                 $b : entity name
        if 'entities' in data and data['entities']:
            for entity in data['entities']:
                record.add_ordered_field(Field(tag='988', indicators=['', ''], subfields=[
                    'a', entity['institution'],
                    'b', entity['entity']
                ]))

        # FUNDINGS section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if 'fundings' in data and data['fundings']:
            for funding in data['fundings']:
                subfields = [
                    'a', funding['organisation'],
                    'e', funding['program'],
                    'f', funding['project']
                ]
                if 'subvention' in funding:
                    subfields.extend(['c', funding['subvention']])
                record.add_ordered_field(Field(tag='536', indicators=['', ''], subfields=subfields))

    @staticmethod
    def record2xml(record):
        # Create ROOT marc:collection tag
        schema_location = "http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"
        root = ET.Element('{http://www.loc.gov/MARC21/slim}collection',
                          attrib={'{http://www.w3.org/2001/XMLSchema-instance}schemaLocation': schema_location},
                          nsmap={
                              'marc': 'http://www.loc.gov/MARC21/slim',
                              'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
                          })
        # transform marc record to marcxml record
        #   ask for 'namespace' into output
        record_xml = marcxml.record_to_xml(record, namespace=True)
        record_xml = ET.fromstring(record_xml)
        # add record data into 'collection' tag
        #   remove 'xsi:schemaLocation' attribute from 'record' tag because it is already present into the root
        #   'collection' tag.
        record_xml.attrib.clear()
        root.append(record_xml)
        return ET.tostring(root, pretty_print=True)


class ArticleRecordBuilder(PublicationRecordBuilder):

    def __init__(self):
        super(ArticleRecordBuilder, self).__init__()

    def json2xml(self, data):
        """
            This function transform some JSON data to a MARC record valid for DIAL. The JSON data should be validate
            by the 'article-schema' jsonschema.

            :param data: the JSON data as a dictionary
            :return: a :class:pymarc.record.MARCRecord object formatted as used into DIAL
        """
        record = self._get_basic_record(data)
        # PUBLICATION_STATUS section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   973 ['', ''] $a : Publication status (accepted, in press, submitted)
        if 'publication_status' in data:
            record.add_ordered_field(Field(tag='973', indicators=['', ''], subfields=[
                'a', data['publication_status']
            ]))
        # DOI section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   856 ['4', '0'] $u : the DOI starting with "10." string
        #                  $z : url type --> always "DOI" in this case
        if 'doi' in data:
            record.add_ordered_field(Field(tag='856', indicators=['4', '0'], subfields=[
                'u', data['doi'],
                'z', 'DOI'
            ]))
        # PUBLISHERS section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   260 ['', ''] $a : publisher/editor place
        #                $b : publication/editor name
        if 'publishers' in data and data['publishers']:
            if record['260'] is None:
                record.add_ordered_field(Field(tag='260', indicators=['', '']))
            datafield = record['260']
            for publisher in data['publishers']:
                if 'name' in publisher:
                    datafield.add_subfield('b', publisher['name'])
                if 'place' in publisher:
                    datafield.add_subfield('a', publisher['place'])
        # JOURNAL ISSUE section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   773 ['', ''] $g : journal issue information (volume, number, pages, year)
        #                $t : the journal title
        #                $n : 'peer-reviewed'
        #   022 ['', ''] $a : issn value
        #                $v : issn type
        if 'journal_issue' in data:
            jdata = data['journal_issue']
            subfields = []
            if 'title' in jdata:
                subfields.extend(['t', jdata['title']])
            if 'peer-reviewed' in jdata and jdata['peer-reviewed'] is True:
                subfields.extend(['n', 'peer-reviewed'])
            if any(j in jdata.keys() for j in ['volume', 'issue', 'page', 'year']):
                issue_data = []
                if 'volume' in jdata:
                    val = re.sub(r'volume|vol[.]?', '', jdata['volume'], re.IGNORECASE)
                    if val is not None and val:
                        issue_data.append("Vol. "+val.strip())
                if 'issue' in jdata:
                    val = re.sub(r'n[o]?[.]?', '', jdata['issue'], re.IGNORECASE)
                    if val is not None and val:
                        issue_data.append("no. "+val.strip())
                if 'page' in jdata:
                    val = re.sub(r'p{1,2}[.]?', '', jdata['page'], re.IGNORECASE)
                    if val is not None and val:
                        issue_data.append("p. "+val.strip())
                issue_data = ', '.join(issue_data)
                if 'year' in jdata and jdata['year'] not in PublicationRecordBuilder.NOT_APPLICABLE:
                    issue_data = issue_data + " ({year})".format(year=jdata['year'])
                subfields.extend(['g', issue_data])
            record.add_ordered_field(Field(tag='773', indicators=['', ''], subfields=subfields))

            if 'issn-type' in jdata and jdata['issn-type']:
                for issn in [d for d in jdata['issn-type'] if 'value' in d]:
                    issn['type'] = issn['type'] if 'type' in issn else 'issn'
                    record.add_ordered_field(Field(tag='022', indicators=['', ''], subfields=[
                        'a', issn['value'],
                        'v', issn['type']
                    ]))
        return record
