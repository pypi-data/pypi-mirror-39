from eulxml import xmlmap
from eulxml.xmlmap import parseString
import pymarc
from StringIO import StringIO


class Marcxml(xmlmap.XmlObject):

    ROOT_NS = 'http://www.loc.gov/MARC21/slim'
    ROOT_NAME = 'collection'
    ROOT_NAMESPACES = {'marc': 'http://www.loc.gov/MARC21/slim'}
    XSD_SCHEMA = 'http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd'

    def __init__(self, *args, **kwargs):
        super(Marcxml, self).__init__(*args, **kwargs)
        records = pymarc.parse_xml_to_array(StringIO(self.serialize()))
        self.marc_data = next(iter(records or []), None)
        self.marc_data.force_utf8 = True

    def serialize(self, stream=None, pretty=False):
        if hasattr(self, 'marc_data'):
            # We need to test if 'marc_data' attribute is available because we use the function 'serialize' to
            # init the self.marc_data attribute.
            # If this attribute is present, it could be updated by user method calls. So we need to use this attribute
            # to serialize this object content instead of the current parent 'self.node' attribute
            new_tag = self._build_root_element()
            node = parseString(pymarc.record_to_xml(self.marc_data))
            new_tag.append(node)
            self.node = new_tag
        return super(Marcxml, self).serialize(stream=stream, pretty=pretty)
