"""This module defines the envelope used to wrap asynchronous messages to be sent to a remote MHS."""
import copy
import re
from typing import Dict, Tuple, Any, Optional, NamedTuple
from xml.etree.ElementTree import Element

import utilities.message_utilities as message_utilities
from utilities import integration_adaptors_logger as log

from mhs_common.messages import envelope

logger = log.IntegrationAdaptorsLogger(__name__)

TEMPLATES_DIR = "data/templates"

FROM_PARTY_ID = "from_party_id"
TO_PARTY_ID = "to_party_id"
CPA_ID = "cpa_id"
CONVERSATION_ID = 'conversation_id'
SERVICE = "service"
ACTION = "action"
MESSAGE_ID = 'message_id'
TIMESTAMP = 'timestamp'
RECEIVED_MESSAGE_ID = "received_message_id"  # RefToMessageId - id of original message sent to outbound
ERROR_CODE = "error_code"
SEVERITY = "severity"
DESCRIPTION = "description"
ATTACHMENTS = "attachments"
EXTERNAL_ATTACHMENTS = "external_attachments"

EXTERNAL_ATTACHMENTS_PARENT = "Manifest"
EXTERNAL_ATTACHMENTS_DESCRIPTION_TAG = "Description"

EXTERNAL_ATTACHMENT_DOCUMENT_ID = 'document_id'
EXTERNAL_ATTACHMENT_MESSAGE_ID = 'message_id'
EXTERNAL_ATTACHMENT_DESCRIPTION = 'description'
EXTERNAL_ATTACHMENT_TITLE = 'title'

ATTACHMENTS_DESCRIPTION_TAG = "Description"

ATTACHMENT_CONTENT_ID = 'content_id'
ATTACHMENT_CONTENT_TYPE = 'content_type'
ATTACHMENT_BASE64 = 'is_base64'
ATTACHMENT_CONTENT_TRANSFER_ENCODING = 'content_transfer_encoding'
ATTACHMENT_PAYLOAD = 'payload'
ATTACHMENT_DESCRIPTION = 'description'

EBXML_NAMESPACE = "eb"
SOAP_NAMESPACE = "SOAP"
XLINK_NAMESPACE = "xlink"

NAMESPACES = {SOAP_NAMESPACE: "http://schemas.xmlsoap.org/soap/envelope/",
              EBXML_NAMESPACE: "http://www.oasis-open.org/committees/ebxml-msg/schema/msg-header-2_0.xsd",
              XLINK_NAMESPACE: "http://www.w3.org/1999/xlink"}


class EbxmlEnvelope(envelope.Envelope):
    """An envelope that contains a message to be sent asynchronously to a remote MHS."""

    class _ElementToExtractWhenParsing(NamedTuple):
        name: str
        xml_name: str
        xml_parent: str = None
        required: bool = True

    _elements_to_extract_when_parsing = [
        _ElementToExtractWhenParsing(FROM_PARTY_ID, 'PartyId', xml_parent='From'),
        _ElementToExtractWhenParsing(TO_PARTY_ID, 'PartyId', xml_parent='To'),
        _ElementToExtractWhenParsing(CPA_ID, 'CPAId'),
        _ElementToExtractWhenParsing(CONVERSATION_ID, 'ConversationId'),
        _ElementToExtractWhenParsing(SERVICE, 'Service'),
        _ElementToExtractWhenParsing(ACTION, 'Action'),
        _ElementToExtractWhenParsing(MESSAGE_ID, 'MessageId', xml_parent='MessageData'),
        _ElementToExtractWhenParsing(TIMESTAMP, 'Timestamp', xml_parent='MessageData'),
        _ElementToExtractWhenParsing(RECEIVED_MESSAGE_ID, 'RefToMessageId', xml_parent='MessageData', required=False),
    ]

    def __init__(self, template_file: str, message_dictionary: Dict[str, Any]):
        super().__init__(template_file, message_dictionary)

    def serialize(self, _message_dictionary: Dict[str, Any] = None) -> Tuple[str, Dict[str, str], str]:
        """Produce a serialised representation of this ebXML message by populating a Mustache template with this
        object's properties.

        :type _message_dictionary: An optional `message_dictionary` to use instead of the one supplied when this
        instance was constructed. For use by subclasses.
        :return: A tuple string containing the message ID, HTTP headers to be sent with the message and the message
        itself.
        """
        ebxml_message_dictionary = copy.deepcopy(_message_dictionary or self.message_dictionary)

        message_id = ebxml_message_dictionary.get(MESSAGE_ID)
        if not message_id:
            message_id = message_utilities.get_uuid()
            ebxml_message_dictionary[MESSAGE_ID] = message_id
        timestamp = message_utilities.get_timestamp()
        ebxml_message_dictionary[TIMESTAMP] = timestamp
        logger.info('Creating ebXML message with {MessageId} and {Timestamp}',
                    fparams={'MessageId': message_id, 'Timestamp': timestamp})

        message = self.message_builder.build_message(ebxml_message_dictionary)
        http_headers = {
            'charset': 'UTF-8',
            'SOAPAction': f'{ebxml_message_dictionary[SERVICE]}/{ebxml_message_dictionary[ACTION]}'
        }
        return message_id, http_headers, message

    @staticmethod
    def _add_if_present(values_dict: Dict[str, Any], key: str, value: Optional[Any]):
        if value is not None:
            values_dict[key] = value

    @staticmethod
    def _add_flag(values_dict: Dict[str, Any], key: str, value: Optional[Any]):
        values_dict[key] = True if value is not None else False

    @staticmethod
    def parse_message(xml_tree: Element) -> Dict[str, str]:
        """Extract a dictionary of values from the provided xml Element tree.

        :param xml_tree: The xml tree to extract values from
        :return: A dictionary of values extracted from the message.
        """
        extracted_values = {}

        for element_to_extract in EbxmlEnvelope._elements_to_extract_when_parsing:
            extracted_value = EbxmlEnvelope._extract_ebxml_text_value(xml_tree,
                                                                      element_to_extract.xml_name,
                                                                      parent=element_to_extract.xml_parent,
                                                                      required=element_to_extract.required)
            EbxmlEnvelope._add_if_present(extracted_values, element_to_extract.name, extracted_value)


        return extracted_values

    @staticmethod
    def parse_attachments(xml_tree: Element, attachment_payloads) -> Dict[str, str]:
        """Extract a dictionary of attachments from the provided xml Element tree.

        :param xml_tree: The xml tree to extract values from
        :param attachments: A dictionary of previously extracted attachment payloads
        :return: A dictionary of values extracted from the message.
        """
        extracted_values = {}

        xpath = EbxmlEnvelope._path_to_ebxml_element(EXTERNAL_ATTACHMENTS_PARENT, None)
        manifestElement = xml_tree.find(xpath, namespaces=NAMESPACES)

        attachments = []
        for child in manifestElement:

            cid_attribute = None
            xpath_description = None 
            description_attribute = None

            if '{'+ NAMESPACES[XLINK_NAMESPACE]+ '}href' in child.attrib:
                cid_attribute = (child.attrib['{'+ NAMESPACES[XLINK_NAMESPACE]+ '}href'])

            if "cid" in cid_attribute:

                xpath_description = EbxmlEnvelope._path_to_ebxml_element(ATTACHMENTS_DESCRIPTION_TAG, None)
                description_attribute = child.find(xpath_description, namespaces=NAMESPACES)

                # it is possible that an attachment does not have a description like in the case of a COPC attachment index file part
                # however, we will take one if we have it
                description = ""
                if description_attribute is not None:
                    if description_attribute.text is not None:
                        description = re.sub(r"[\n\t]*", "", description_attribute.text)

                cid = cid_attribute.split(":")[1]
                # grab the existing payload item by cid
                foundPayload = next((item for item in attachment_payloads if item[ATTACHMENT_CONTENT_ID] == cid), None)

                # We may have already decompressed a compressed payload or converted from base64, if so,
                # update the payload description fields with the correct details and form our attachment
                # All this to add the description field :)

                if (foundPayload is not None):

                    attachment = {
                        ATTACHMENT_PAYLOAD: foundPayload[ATTACHMENT_PAYLOAD],
                        ATTACHMENT_BASE64: foundPayload[ATTACHMENT_BASE64],
                        ATTACHMENT_CONTENT_ID: foundPayload[ATTACHMENT_CONTENT_ID],
                        ATTACHMENT_CONTENT_TYPE: foundPayload[ATTACHMENT_CONTENT_TYPE],
                        ATTACHMENT_DESCRIPTION: description.strip()
                    }

                    attachments.append(attachment)

        EbxmlEnvelope._add_if_present(extracted_values, ATTACHMENTS, attachments)
        return extracted_values

    @staticmethod
    def parse_external_attachments(xml_tree: Element) -> Dict[str, str]:
        """Extract a dictionary of external attachments from the provided xml Element tree.

        :param xml_tree: The xml tree to extract values from
        :return: A dictionary of values extracted from the message.
        """
        extracted_values = {}

        xpath = EbxmlEnvelope._path_to_ebxml_element(EXTERNAL_ATTACHMENTS_PARENT, None)
        manifestElement = xml_tree.find(xpath, namespaces=NAMESPACES)

        external_attachments = []
        for child in manifestElement:

            mid_attribute = None
            document_id_attribute = None
            xpath_description = None 
            description_attribute = None

            if '{'+ NAMESPACES[XLINK_NAMESPACE]+ '}href' in child.attrib:
                mid_attribute = (child.attrib['{'+ NAMESPACES[XLINK_NAMESPACE]+ '}href'])

            if "mid" in mid_attribute:
                if '{'+ NAMESPACES[EBXML_NAMESPACE]+ '}id' in child.attrib:
                    document_id_attribute = (child.attrib['{'+ NAMESPACES[EBXML_NAMESPACE]+ '}id'])

                xpath_description = EbxmlEnvelope._path_to_ebxml_element(EXTERNAL_ATTACHMENTS_DESCRIPTION_TAG, None)
                description_attribute = child.find(xpath_description, namespaces=NAMESPACES)

                if description_attribute is not None:
                    description = re.sub(r"[\n\t]*", "", description_attribute.text)

                    variables = descriptionParams = re.findall("(?:\".*?\"|\S)+", description.strip())

                    filename = None
                    description_variables = dict(pair.split("=", 1) for pair in variables)
                    if "Filename" in description_variables:
                        filename = description_variables["Filename"].replace('\\', '')

                    mid = mid_attribute.split(":")[1]
                    external_attachment = {
                        EXTERNAL_ATTACHMENT_DOCUMENT_ID :document_id_attribute, 
                        EXTERNAL_ATTACHMENT_MESSAGE_ID :mid_attribute.split(":")[1], 
                        EXTERNAL_ATTACHMENT_DESCRIPTION: description,
                        EXTERNAL_ATTACHMENT_TITLE: filename 
                    }

                    external_attachments.append(external_attachment)

        EbxmlEnvelope._add_if_present(extracted_values, EXTERNAL_ATTACHMENTS, external_attachments)
        return extracted_values
    
    @staticmethod
    def _path_to_ebxml_element(name: str, parent: str = None) -> str:
        path = ".//"

        if parent is not None:
            path += f"{EBXML_NAMESPACE}:{parent}/"

        path += f"{EBXML_NAMESPACE}:{name}"

        return path

    @staticmethod
    def _extract_ebxml_value(xml_tree: Element, element_name: str, parent: str = None,
                             required: bool = False) -> Optional[Element]:
        xpath = EbxmlEnvelope._path_to_ebxml_element(element_name, parent=parent)

        value = xml_tree.find(xpath, namespaces=NAMESPACES)
            
        if value is None and required:
            logger.error("Weren't able to find required element {xpath} during parsing of EbXML message.",
                         fparams={'xpath': xpath})
            raise EbXmlParsingError(f"Weren't able to find required element {xpath} during parsing of EbXML message")
        return value
   
    @staticmethod
    def _extract_ebxml_text_value(xml_tree: Element, element_name: str, parent: str = None,
                                  required: bool = False) -> Optional[str]:
        value = EbxmlEnvelope._extract_ebxml_value(xml_tree, element_name, parent, required)
        text = None

        if value is not None:
            text = value.text

        return text

    @staticmethod
    def _extract_attribute(xml_tree: Element, element_name: str, attribute_namespace: Dict[str, str],
                           attribute_name: str, values_dict: Dict[str, Any], key: str):
        xpath = EbxmlEnvelope._path_to_ebxml_element(element_name)
        element = xml_tree.find(xpath, NAMESPACES)
        if element is not None:
            try:
                values_dict[key] = element.attrib["{" + NAMESPACES[attribute_namespace] + "}" + attribute_name]
            except KeyError as e:
                logger.error("Weren't able to find required {attribute_name} of {xpath} during parsing of "
                             "EbXML message.", fparams={'attribute_name': attribute_name, 'xpath': xpath})
                raise EbXmlParsingError(f"Weren't able to find required attribute {attribute_name} during parsing of "
                                        f"EbXML message") from e

class EbXmlParsingError(Exception):
    """Raised when an error was encountered during parsing of an ebXML message."""
    pass
