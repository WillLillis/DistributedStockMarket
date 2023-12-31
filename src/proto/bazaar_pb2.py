# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bazaar.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62\x61zaar.proto\x1a\x1bgoogle/protobuf/empty.proto\"#\n\rLookupRequest\x12\x12\n\nstock_name\x18\x01 \x01(\t\"U\n\x0eLookupResponse\x12\r\n\x05price\x18\x01 \x01(\x02\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x0e\n\x06volume\x18\x03 \x01(\x05\x12\x12\n\nmax_volume\x18\x04 \x01(\x05\"K\n\x0cOrderRequest\x12\x12\n\nstock_name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x15\n\x04type\x18\x03 \x01(\x0e\x32\x07.Action\"+\n\rOrderResponse\x12\x1a\n\x12transaction_number\x18\x01 \x01(\x05\"N\n\rUpdateRequest\x12\x12\n\nstock_name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x17\n\x06\x61\x63tion\x18\x03 \x01(\x0e\x32\x07.Action\" \n\x0eUpdateResponse\x12\x0e\n\x06status\x18\x01 \x01(\x05\"\'\n\x0fGetOrderRequest\x12\x14\n\x0corder_number\x18\x01 \x01(\x05\"_\n\x10GetOrderResponse\x12\x14\n\x0corder_number\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\x04type\x18\x03 \x01(\x0e\x32\x07.Action\x12\x10\n\x08quantity\x18\x04 \x01(\x05\"&\n\x13HealthCheckResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"/\n\x18SignalOrderLeaderRequest\x12\x13\n\x0bleader_port\x18\x01 \x01(\x05\",\n\x19SignalOrderLeaderResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"p\n\x15\x46ollowerUpdateRequest\x12\x12\n\nstock_name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x15\n\x04type\x18\x03 \x01(\x0e\x32\x07.Action\x12\x1a\n\x12transaction_number\x18\x04 \x01(\x05\")\n\x16\x46ollowerUpdateResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"4\n\x16OrderLogRecoverRequest\x12\x1a\n\x12transaction_number\x18\x01 \x01(\x05\"\xca\x01\n\x17OrderLogRecoverResponse\x12>\n\x07\x65ntries\x18\x01 \x03(\x0b\x32-.OrderLogRecoverResponse.OrderLogRecoverEntry\x1ao\n\x14OrderLogRecoverEntry\x12\x1a\n\x12transaction_number\x18\x01 \x01(\x05\x12\x12\n\nstock_name\x18\x02 \x01(\t\x12\x15\n\x04type\x18\x03 \x01(\x0e\x32\x07.Action\x12\x10\n\x08quantity\x18\x04 \x01(\x05*\x1b\n\x06\x41\x63tion\x12\x07\n\x03\x42UY\x10\x00\x12\x08\n\x04SELL\x10\x01\x32\xd9\x03\n\x06\x42\x61zaar\x12+\n\x06Lookup\x12\x0e.LookupRequest\x1a\x0f.LookupResponse\"\x00\x12(\n\x05Order\x12\r.OrderRequest\x1a\x0e.OrderResponse\"\x00\x12+\n\x06Update\x12\x0e.UpdateRequest\x1a\x0f.UpdateResponse\"\x00\x12\x31\n\x08GetOrder\x12\x10.GetOrderRequest\x1a\x11.GetOrderResponse\"\x00\x12=\n\x0bHealthCheck\x12\x16.google.protobuf.Empty\x1a\x14.HealthCheckResponse\"\x00\x12L\n\x11SignalOrderLeader\x12\x19.SignalOrderLeaderRequest\x1a\x1a.SignalOrderLeaderResponse\"\x00\x12\x43\n\x0e\x46ollowerUpdate\x12\x16.FollowerUpdateRequest\x1a\x17.FollowerUpdateResponse\"\x00\x12\x46\n\x0fOrderLogRecover\x12\x17.OrderLogRecoverRequest\x1a\x18.OrderLogRecoverResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bazaar_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACTION._serialized_start=1094
  _ACTION._serialized_end=1121
  _LOOKUPREQUEST._serialized_start=45
  _LOOKUPREQUEST._serialized_end=80
  _LOOKUPRESPONSE._serialized_start=82
  _LOOKUPRESPONSE._serialized_end=167
  _ORDERREQUEST._serialized_start=169
  _ORDERREQUEST._serialized_end=244
  _ORDERRESPONSE._serialized_start=246
  _ORDERRESPONSE._serialized_end=289
  _UPDATEREQUEST._serialized_start=291
  _UPDATEREQUEST._serialized_end=369
  _UPDATERESPONSE._serialized_start=371
  _UPDATERESPONSE._serialized_end=403
  _GETORDERREQUEST._serialized_start=405
  _GETORDERREQUEST._serialized_end=444
  _GETORDERRESPONSE._serialized_start=446
  _GETORDERRESPONSE._serialized_end=541
  _HEALTHCHECKRESPONSE._serialized_start=543
  _HEALTHCHECKRESPONSE._serialized_end=581
  _SIGNALORDERLEADERREQUEST._serialized_start=583
  _SIGNALORDERLEADERREQUEST._serialized_end=630
  _SIGNALORDERLEADERRESPONSE._serialized_start=632
  _SIGNALORDERLEADERRESPONSE._serialized_end=676
  _FOLLOWERUPDATEREQUEST._serialized_start=678
  _FOLLOWERUPDATEREQUEST._serialized_end=790
  _FOLLOWERUPDATERESPONSE._serialized_start=792
  _FOLLOWERUPDATERESPONSE._serialized_end=833
  _ORDERLOGRECOVERREQUEST._serialized_start=835
  _ORDERLOGRECOVERREQUEST._serialized_end=887
  _ORDERLOGRECOVERRESPONSE._serialized_start=890
  _ORDERLOGRECOVERRESPONSE._serialized_end=1092
  _ORDERLOGRECOVERRESPONSE_ORDERLOGRECOVERENTRY._serialized_start=981
  _ORDERLOGRECOVERRESPONSE_ORDERLOGRECOVERENTRY._serialized_end=1092
  _BAZAAR._serialized_start=1124
  _BAZAAR._serialized_end=1597
# @@protoc_insertion_point(module_scope)
