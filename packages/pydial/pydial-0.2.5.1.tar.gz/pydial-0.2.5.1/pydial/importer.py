from jsonschema import Draft4Validator, RefResolver
from jsonschema.exceptions import ValidationError

import json
import os


class DataImporter:

    def __init__(self, schemas_directory='./schemas'):
        self.schema_store = {}
        for fname in [fname for fname in os.listdir(schemas_directory) if fname.endswith('.json')]:
            with open(os.path.join(schemas_directory, fname), 'r') as fh:
                schema = json.load(fh)
                if '$id' in schema:
                    Draft4Validator.check_schema(schema)
                    self.schema_store[schema['$id']] = schema
        self.resolver = RefResolver('', '', self.schema_store)

    def _found_specific_schema(self, document_type):
        return [v for k, v in self.schema_store.items() if self._schema_get_document_type(v) == document_type]

    def _schema_get_document_type(self, schema):
        if "properties" in schema:
            if "type" in schema['properties']\
               and "properties" in schema['properties']['type']\
               and "document_type" in schema['properties']['type']['properties']:
                doc_type = schema['properties']['type']['properties']['document_type']
                if 'enum' in doc_type:
                    return next(iter(doc_type['enum']), None)
        elif "allOf" in schema:
            for sub_schema in schema['allOf']:
                doc_type = self._schema_get_document_type(sub_schema)
                if doc_type is not None:
                    return doc_type

    def validate_data(self, json_data):
        """This method will validate the json data according the the document type.

           This method need to use a different jsonschema according of the main document type into the json_data.
           As each dial document jsonschema inherit from 'basics-publications' schema, we can first validate the
           json_data according to this schema. If validation of this schema is successfully, we know that the key
           `json_data['type']['document_type']` exists (it's a required property). So we can use this value to determine
           the right jsonschema according to the found main document type.

           :param json_data: Data to validate. Should represent a dial publication according to jsonschemas
           :type json_data: dict

           :raise `jsonschema.exception.ValidationError: if some error occured during the data validation.
        """
        try:
            basic_schema = self.schema_store.get("http://dial.uclouvain.be/schemas/basics-publications.json")
            Draft4Validator(basic_schema, resolver=self.resolver).validate(json_data)
            matching_schemas = self._found_specific_schema(json_data['type']['document_type'])
            for schema in matching_schemas:
                Draft4Validator(schema, resolver=self.resolver).validate(json_data)
        except ValidationError as ve:
            # TODO : do something better when ValidationError is catched
            raise ve

    def _check_double(self, json_data):
        """
            This function will check if a publication already exists into DIAL based on json_data received.
            !!! If a double candidate is found, this publication shouldn't be added into DIAL.

            :param json_data: data used to search about a double candidate
            :return: True if a double is found, False otherwise.
            :rtype: boolean
        """
        # TODO : create code for check_double..... not simple
        return False

    def _ingest_object(self, json_data):
        """ This function create an new object into DIAL using the jsondata to determine the object type and object
            metadata. All necessary datastream and relations will be created but no attached filed will be added !
            To attach some content file (PDF, DOCX, ZIP, ...) use the 'add_file()' module function

            :param json_data: data containing all necessary metadata about the publication. These data must be validated
                              by 'validate_data()' module function before ingest them into DIAL
        """