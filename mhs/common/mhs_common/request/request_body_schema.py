"""
Schema definition for the request body that MHS accepts. To use this module, simply do:

.. code-block:: python

    try:
        request_body = RequestBodySchema().loads(body)
    except json.JSONDecodeError as e:
        ... # handle JSON decode errors
    except marshmallow.ValidationError as e:
        ... # handle validation errors
"""
import dataclasses
from typing import List

import os
import marshmallow.validate
import utilities.integration_adaptors_logger as log

logger = log.IntegrationAdaptorsLogger(__name__)

# These allowed content types for attachments are taken from the EIS part 2.5.4.2
_ATTACHMENT_ALLOWED_CONTENT_TYPES = tuple(os.environ.get('SUPPORTED_FILE_TYPES').split(","))

if _ATTACHMENT_ALLOWED_CONTENT_TYPES is None:
    logger.error("SUPPORTED_FILE_TYPES not set, please set the SUPPORTED_FILE_TYPES environment variable.")
    _ATTACHMENT_ALLOWED_CONTENT_TYPES = ''


@dataclasses.dataclass
class Attachment:
    """
    Dataclass representing an attachment in the request body that MHS accepts.
    `AttachmentSchema` deserialises to this class.
    """
    is_base64: bool
    content_type: str
    payload: str
    description: str
    document_id: str


class AttachmentSchema(marshmallow.Schema):
    """Schema for an attachment in the request body that MHS accepts"""
    is_base64 = marshmallow.fields.Bool(required=True,
                                        description='Whether the attachment payload is base64-encoded or not. This is '
                                                    'only required for binary attachments eg images.',
                                        truthy={True}, falsy={False})
    content_type = marshmallow.fields.Str(required=True, description='Content type of the attachment',
                                          validate=marshmallow.validate.OneOf(_ATTACHMENT_ALLOWED_CONTENT_TYPES))
    payload = marshmallow.fields.Str(required=True,
                                     description='The attachment, possibly base64-encoded as per is_base64.',
                                     # Max length of payload is 5MB ie 5 000 000 characters. This requirement is from
                                     # EIS section 2.5.4.2
                                     validate=marshmallow.validate.Length(min=1, max=5_000_000))
    description = marshmallow.fields.Str(required=True, description='Description of the attachment',
                                         validate=marshmallow.validate.Length(min=1))
    document_id = marshmallow.fields.Str(required=False,
                                         description='The document id of the attachment.')

    @marshmallow.post_load
    def make_attachment(self, data, **kwargs):
        return Attachment(data['is_base64'],
                          data['content_type'],
                          data['payload'],
                          data['description'],
                          data.get('document_id') or [])


@dataclasses.dataclass
class ExternalAttachment:
    """
    Dataclass representing an external attachment in the request body that MHS accepts.
    `ExternalAttachmentSchema` deserialises to this class.
    """
    document_id: str
    message_id: str
    description: str
    title: str


class ExternalAttachmentSchema(marshmallow.Schema):
    """Schema for an external attachment in the request body that MHS accepts"""
    document_id = marshmallow.fields.Str(required=False,
                                         description='The document id of the attachment.')
    message_id = marshmallow.fields.Str(required=True,
                                        description='Attachment message id.')
    description = marshmallow.fields.Str(required=True, description='Description of the attachment')

    @marshmallow.post_load
    def make_external_attachment(self, data, **kwargs):
        return ExternalAttachment(data.get('document_id') or [], data['message_id'], data['description'],
                                  data.get('title') or '')


@dataclasses.dataclass
class RequestBody:
    """Dataclass representing the request body that MHS accepts. `RequestBodySchema` deserialises to this class."""
    payload: str
    attachments: List[Attachment]
    external_attachments: List[ExternalAttachment]


class RequestBodySchema(marshmallow.Schema):
    """Schema for the request body that MHS accepts"""
    payload = marshmallow.fields.Str(
        required=True, description='HL7 Payload to send to Spine',
        # No explicit documentation was found in the EIS as to the max size of this
        # HL7 payload, but additional attachments have a max size of 5MB so just set to
        # this. Note that the whole request body sent to Spine gets checked later to make
        # sure it isn't too large.
        validate=marshmallow.validate.Length(min=1, max=5_000_000))
    attachments = marshmallow.fields.Nested(
        AttachmentSchema, many=True, missing=[],
        description='Optional attachments to send with the payload. Only for use '
                    'for interactions that support sending attachments.',
        # EIS 2.5.4.2 says that the max number of attachments is 100, including
        # the ebXML MIME part. And there is also the HL7 payload, so 100 - 2 = 98
        validate=marshmallow.validate.Length(max=98))
    external_attachments = marshmallow.fields.Nested(
        ExternalAttachmentSchema, many=True, missing=[],
        description='Optional external attachments to include in the Manifest '
                    'that will be sent in separate messages. Only for use '
                    'for interactions that support sending attachments.',
        # EIS 2.5.4.2 says that the max number of attachments is 100, including
        # the ebXML MIME part. And there is also the HL7 payload, so 100 - 2 = 98
        validate=marshmallow.validate.Length(max=98))

    @marshmallow.post_load
    def make_request_body(self, data, **kwargs):
        return RequestBody(data['payload'], data['attachments'], data['external_attachments'])
