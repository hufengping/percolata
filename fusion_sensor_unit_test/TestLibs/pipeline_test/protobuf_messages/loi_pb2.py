# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: loi.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='loi.proto',
  package='',
  serialized_pb='\n\tloi.proto\"\xc4\x02\n\x0fLOIPedCountData\x12\x15\n\rplacementName\x18\x01 \x02(\t\x12\x0e\n\x06viewId\x18\x02 \x02(\x05\x12\x16\n\x0estartTimestamp\x18\x03 \x02(\x12\x12\x14\n\x0c\x65ndTimestamp\x18\x04 \x02(\x12\x12\x12\n\nframeCount\x18\x05 \x02(\r\x12\x31\n\x06\x65vents\x18\x06 \x03(\x0b\x32!.LOIPedCountData.LOIPedCountEvent\x1a\x94\x01\n\x10LOIPedCountEvent\x12\x16\n\x0e\x65ventTimestamp\x18\x01 \x02(\x12\x12\x11\n\tdirection\x18\x02 \x02(\x05\x12\x13\n\x0bloiPosition\x18\x03 \x02(\r\x12\x12\n\neventWidth\x18\x04 \x02(\r\x12\x14\n\x0cweightedArea\x18\x05 \x02(\x01\x12\x16\n\x0e\x65stimatedCount\x18\x06 \x02(\x01\"\xbe\x02\n\x15LOIForegroundBlobData\x12\x15\n\rplacementName\x18\x01 \x02(\t\x12\x0e\n\x06viewId\x18\x02 \x02(\x05\x12\x15\n\rminPersonArea\x18\x03 \x02(\x05\x12\x1a\n\x12\x65xpectedPersonArea\x18\x04 \x02(\x05\x12\x16\n\x0estartTimestamp\x18\x05 \x02(\x12\x12\x14\n\x0c\x65ndTimestamp\x18\x06 \x02(\x12\x12\x12\n\nframeCount\x18\x07 \x02(\r\x12*\n\x05\x62lobs\x18\x08 \x03(\x0b\x32\x1b.LOIForegroundBlobData.Blob\x1a]\n\x04\x42lob\x12\x11\n\tstartLine\x18\x01 \x02(\r\x12\r\n\x05width\x18\x02 \x02(\r\x12\x18\n\x10leftWeightedArea\x18\x03 \x02(\x01\x12\x19\n\x11rightWeightedArea\x18\x04 \x02(\x01')




_LOIPEDCOUNTDATA_LOIPEDCOUNTEVENT = _descriptor.Descriptor(
  name='LOIPedCountEvent',
  full_name='LOIPedCountData.LOIPedCountEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='eventTimestamp', full_name='LOIPedCountData.LOIPedCountEvent.eventTimestamp', index=0,
      number=1, type=18, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='direction', full_name='LOIPedCountData.LOIPedCountEvent.direction', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='loiPosition', full_name='LOIPedCountData.LOIPedCountEvent.loiPosition', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eventWidth', full_name='LOIPedCountData.LOIPedCountEvent.eventWidth', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weightedArea', full_name='LOIPedCountData.LOIPedCountEvent.weightedArea', index=4,
      number=5, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='estimatedCount', full_name='LOIPedCountData.LOIPedCountEvent.estimatedCount', index=5,
      number=6, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=190,
  serialized_end=338,
)

_LOIPEDCOUNTDATA = _descriptor.Descriptor(
  name='LOIPedCountData',
  full_name='LOIPedCountData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='placementName', full_name='LOIPedCountData.placementName', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='viewId', full_name='LOIPedCountData.viewId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='startTimestamp', full_name='LOIPedCountData.startTimestamp', index=2,
      number=3, type=18, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endTimestamp', full_name='LOIPedCountData.endTimestamp', index=3,
      number=4, type=18, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frameCount', full_name='LOIPedCountData.frameCount', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='events', full_name='LOIPedCountData.events', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_LOIPEDCOUNTDATA_LOIPEDCOUNTEVENT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=14,
  serialized_end=338,
)


_LOIFOREGROUNDBLOBDATA_BLOB = _descriptor.Descriptor(
  name='Blob',
  full_name='LOIForegroundBlobData.Blob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='startLine', full_name='LOIForegroundBlobData.Blob.startLine', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width', full_name='LOIForegroundBlobData.Blob.width', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='leftWeightedArea', full_name='LOIForegroundBlobData.Blob.leftWeightedArea', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rightWeightedArea', full_name='LOIForegroundBlobData.Blob.rightWeightedArea', index=3,
      number=4, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=566,
  serialized_end=659,
)

_LOIFOREGROUNDBLOBDATA = _descriptor.Descriptor(
  name='LOIForegroundBlobData',
  full_name='LOIForegroundBlobData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='placementName', full_name='LOIForegroundBlobData.placementName', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='viewId', full_name='LOIForegroundBlobData.viewId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='minPersonArea', full_name='LOIForegroundBlobData.minPersonArea', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expectedPersonArea', full_name='LOIForegroundBlobData.expectedPersonArea', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='startTimestamp', full_name='LOIForegroundBlobData.startTimestamp', index=4,
      number=5, type=18, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endTimestamp', full_name='LOIForegroundBlobData.endTimestamp', index=5,
      number=6, type=18, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frameCount', full_name='LOIForegroundBlobData.frameCount', index=6,
      number=7, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='blobs', full_name='LOIForegroundBlobData.blobs', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_LOIFOREGROUNDBLOBDATA_BLOB, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=341,
  serialized_end=659,
)

_LOIPEDCOUNTDATA_LOIPEDCOUNTEVENT.containing_type = _LOIPEDCOUNTDATA;
_LOIPEDCOUNTDATA.fields_by_name['events'].message_type = _LOIPEDCOUNTDATA_LOIPEDCOUNTEVENT
_LOIFOREGROUNDBLOBDATA_BLOB.containing_type = _LOIFOREGROUNDBLOBDATA;
_LOIFOREGROUNDBLOBDATA.fields_by_name['blobs'].message_type = _LOIFOREGROUNDBLOBDATA_BLOB
DESCRIPTOR.message_types_by_name['LOIPedCountData'] = _LOIPEDCOUNTDATA
DESCRIPTOR.message_types_by_name['LOIForegroundBlobData'] = _LOIFOREGROUNDBLOBDATA

class LOIPedCountData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class LOIPedCountEvent(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _LOIPEDCOUNTDATA_LOIPEDCOUNTEVENT

    # @@protoc_insertion_point(class_scope:LOIPedCountData.LOIPedCountEvent)
  DESCRIPTOR = _LOIPEDCOUNTDATA

  # @@protoc_insertion_point(class_scope:LOIPedCountData)

class LOIForegroundBlobData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class Blob(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _LOIFOREGROUNDBLOBDATA_BLOB

    # @@protoc_insertion_point(class_scope:LOIForegroundBlobData.Blob)
  DESCRIPTOR = _LOIFOREGROUNDBLOBDATA

  # @@protoc_insertion_point(class_scope:LOIForegroundBlobData)


# @@protoc_insertion_point(module_scope)
