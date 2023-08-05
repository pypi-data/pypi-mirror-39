# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ortools/constraint_solver/model.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ortools.constraint_solver import search_limit_pb2 as ortools_dot_constraint__solver_dot_search__limit__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ortools/constraint_solver/model.proto',
  package='operations_research',
  syntax='proto3',
  serialized_options=_b('\n#com.google.ortools.constraintsolverP\001\252\002\037Google.OrTools.ConstraintSolver'),
  serialized_pb=_b('\n%ortools/constraint_solver/model.proto\x12\x13operations_research\x1a,ortools/constraint_solver/search_limit.proto\"@\n\x0f\x43pIntegerMatrix\x12\x0c\n\x04rows\x18\x01 \x01(\x05\x12\x0f\n\x07\x63olumns\x18\x02 \x01(\x05\x12\x0e\n\x06values\x18\x03 \x03(\x03\"\xa4\x04\n\nCpArgument\x12\x16\n\x0e\x61rgument_index\x18\x01 \x01(\x05\x12\x15\n\rinteger_value\x18\x02 \x01(\x03\x12\x15\n\rinteger_array\x18\x03 \x03(\x03\x12 \n\x18integer_expression_index\x18\x04 \x01(\x05\x12 \n\x18integer_expression_array\x18\x05 \x03(\x05\x12\x16\n\x0einterval_index\x18\x06 \x01(\x05\x12\x16\n\x0einterval_array\x18\x07 \x03(\x05\x12\x16\n\x0esequence_index\x18\x08 \x01(\x05\x12\x16\n\x0esequence_array\x18\t \x03(\x05\x12<\n\x0einteger_matrix\x18\n \x01(\x0b\x32$.operations_research.CpIntegerMatrix\x12\x32\n\x04type\x18\x0b \x01(\x0e\x32$.operations_research.CpArgument.Type\"\xb9\x01\n\x04Type\x12\r\n\tUNDEFINED\x10\x00\x12\x11\n\rINTEGER_VALUE\x10\x01\x12\x11\n\rINTEGER_ARRAY\x10\x02\x12\x0e\n\nEXPRESSION\x10\x03\x12\x14\n\x10\x45XPRESSION_ARRAY\x10\x04\x12\x0c\n\x08INTERVAL\x10\x05\x12\x12\n\x0eINTERVAL_ARRAY\x10\x06\x12\x0c\n\x08SEQUENCE\x10\x07\x12\x12\n\x0eSEQUENCE_ARRAY\x10\x08\x12\x12\n\x0eINTEGER_MATRIX\x10\t\"U\n\x0b\x43pExtension\x12\x12\n\ntype_index\x18\x01 \x01(\x05\x12\x32\n\targuments\x18\x02 \x03(\x0b\x32\x1f.operations_research.CpArgument\"\xb0\x01\n\x13\x43pIntegerExpression\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x12\n\ntype_index\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x32\n\targuments\x18\x04 \x03(\x0b\x32\x1f.operations_research.CpArgument\x12\x34\n\nextensions\x18\x05 \x03(\x0b\x32 .operations_research.CpExtension\"y\n\x12\x43pIntervalVariable\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x12\n\ntype_index\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x32\n\targuments\x18\x04 \x03(\x0b\x32\x1f.operations_research.CpArgument\"y\n\x12\x43pSequenceVariable\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x12\n\ntype_index\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x32\n\targuments\x18\x04 \x03(\x0b\x32\x1f.operations_research.CpArgument\"\xa9\x01\n\x0c\x43pConstraint\x12\r\n\x05index\x18\x01 \x01(\x05\x12\x12\n\ntype_index\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x32\n\targuments\x18\x04 \x03(\x0b\x32\x1f.operations_research.CpArgument\x12\x34\n\nextensions\x18\x05 \x03(\x0b\x32 .operations_research.CpExtension\"F\n\x0b\x43pObjective\x12\x10\n\x08maximize\x18\x01 \x01(\x08\x12\x0c\n\x04step\x18\x02 \x01(\x03\x12\x17\n\x0fobjective_index\x18\x03 \x01(\x05\"S\n\x0f\x43pVariableGroup\x12\x32\n\targuments\x18\x01 \x03(\x0b\x32\x1f.operations_research.CpArgument\x12\x0c\n\x04type\x18\x02 \x01(\t\"\xf2\x03\n\x07\x43pModel\x12\r\n\x05model\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x0c\n\x04tags\x18\x03 \x03(\t\x12=\n\x0b\x65xpressions\x18\x04 \x03(\x0b\x32(.operations_research.CpIntegerExpression\x12:\n\tintervals\x18\x05 \x03(\x0b\x32\'.operations_research.CpIntervalVariable\x12:\n\tsequences\x18\x06 \x03(\x0b\x32\'.operations_research.CpSequenceVariable\x12\x36\n\x0b\x63onstraints\x18\x07 \x03(\x0b\x32!.operations_research.CpConstraint\x12\x33\n\tobjective\x18\x08 \x01(\x0b\x32 .operations_research.CpObjective\x12@\n\x0csearch_limit\x18\t \x01(\x0b\x32*.operations_research.SearchLimitParameters\x12=\n\x0fvariable_groups\x18\n \x03(\x0b\x32$.operations_research.CpVariableGroup\x12\x14\n\x0clicense_text\x18\x0b \x01(\tBI\n#com.google.ortools.constraintsolverP\x01\xaa\x02\x1fGoogle.OrTools.ConstraintSolverb\x06proto3')
  ,
  dependencies=[ortools_dot_constraint__solver_dot_search__limit__pb2.DESCRIPTOR,])



_CPARGUMENT_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='operations_research.CpArgument.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTEGER_VALUE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTEGER_ARRAY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXPRESSION', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXPRESSION_ARRAY', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTERVAL', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTERVAL_ARRAY', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEQUENCE', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEQUENCE_ARRAY', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTEGER_MATRIX', index=9, number=9,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=538,
  serialized_end=723,
)
_sym_db.RegisterEnumDescriptor(_CPARGUMENT_TYPE)


_CPINTEGERMATRIX = _descriptor.Descriptor(
  name='CpIntegerMatrix',
  full_name='operations_research.CpIntegerMatrix',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rows', full_name='operations_research.CpIntegerMatrix.rows', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='columns', full_name='operations_research.CpIntegerMatrix.columns', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='values', full_name='operations_research.CpIntegerMatrix.values', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=108,
  serialized_end=172,
)


_CPARGUMENT = _descriptor.Descriptor(
  name='CpArgument',
  full_name='operations_research.CpArgument',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='argument_index', full_name='operations_research.CpArgument.argument_index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='integer_value', full_name='operations_research.CpArgument.integer_value', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='integer_array', full_name='operations_research.CpArgument.integer_array', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='integer_expression_index', full_name='operations_research.CpArgument.integer_expression_index', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='integer_expression_array', full_name='operations_research.CpArgument.integer_expression_array', index=4,
      number=5, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='interval_index', full_name='operations_research.CpArgument.interval_index', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='interval_array', full_name='operations_research.CpArgument.interval_array', index=6,
      number=7, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sequence_index', full_name='operations_research.CpArgument.sequence_index', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sequence_array', full_name='operations_research.CpArgument.sequence_array', index=8,
      number=9, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='integer_matrix', full_name='operations_research.CpArgument.integer_matrix', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='operations_research.CpArgument.type', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CPARGUMENT_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=175,
  serialized_end=723,
)


_CPEXTENSION = _descriptor.Descriptor(
  name='CpExtension',
  full_name='operations_research.CpExtension',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type_index', full_name='operations_research.CpExtension.type_index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='operations_research.CpExtension.arguments', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=725,
  serialized_end=810,
)


_CPINTEGEREXPRESSION = _descriptor.Descriptor(
  name='CpIntegerExpression',
  full_name='operations_research.CpIntegerExpression',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='operations_research.CpIntegerExpression.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_index', full_name='operations_research.CpIntegerExpression.type_index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.CpIntegerExpression.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='operations_research.CpIntegerExpression.arguments', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extensions', full_name='operations_research.CpIntegerExpression.extensions', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=813,
  serialized_end=989,
)


_CPINTERVALVARIABLE = _descriptor.Descriptor(
  name='CpIntervalVariable',
  full_name='operations_research.CpIntervalVariable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='operations_research.CpIntervalVariable.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_index', full_name='operations_research.CpIntervalVariable.type_index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.CpIntervalVariable.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='operations_research.CpIntervalVariable.arguments', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=991,
  serialized_end=1112,
)


_CPSEQUENCEVARIABLE = _descriptor.Descriptor(
  name='CpSequenceVariable',
  full_name='operations_research.CpSequenceVariable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='operations_research.CpSequenceVariable.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_index', full_name='operations_research.CpSequenceVariable.type_index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.CpSequenceVariable.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='operations_research.CpSequenceVariable.arguments', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1114,
  serialized_end=1235,
)


_CPCONSTRAINT = _descriptor.Descriptor(
  name='CpConstraint',
  full_name='operations_research.CpConstraint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='operations_research.CpConstraint.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_index', full_name='operations_research.CpConstraint.type_index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.CpConstraint.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arguments', full_name='operations_research.CpConstraint.arguments', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extensions', full_name='operations_research.CpConstraint.extensions', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1238,
  serialized_end=1407,
)


_CPOBJECTIVE = _descriptor.Descriptor(
  name='CpObjective',
  full_name='operations_research.CpObjective',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='maximize', full_name='operations_research.CpObjective.maximize', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='step', full_name='operations_research.CpObjective.step', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='objective_index', full_name='operations_research.CpObjective.objective_index', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1409,
  serialized_end=1479,
)


_CPVARIABLEGROUP = _descriptor.Descriptor(
  name='CpVariableGroup',
  full_name='operations_research.CpVariableGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arguments', full_name='operations_research.CpVariableGroup.arguments', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='operations_research.CpVariableGroup.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1481,
  serialized_end=1564,
)


_CPMODEL = _descriptor.Descriptor(
  name='CpModel',
  full_name='operations_research.CpModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='operations_research.CpModel.model', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='operations_research.CpModel.version', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tags', full_name='operations_research.CpModel.tags', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expressions', full_name='operations_research.CpModel.expressions', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='intervals', full_name='operations_research.CpModel.intervals', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sequences', full_name='operations_research.CpModel.sequences', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='operations_research.CpModel.constraints', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='objective', full_name='operations_research.CpModel.objective', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='search_limit', full_name='operations_research.CpModel.search_limit', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='variable_groups', full_name='operations_research.CpModel.variable_groups', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='license_text', full_name='operations_research.CpModel.license_text', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1567,
  serialized_end=2065,
)

_CPARGUMENT.fields_by_name['integer_matrix'].message_type = _CPINTEGERMATRIX
_CPARGUMENT.fields_by_name['type'].enum_type = _CPARGUMENT_TYPE
_CPARGUMENT_TYPE.containing_type = _CPARGUMENT
_CPEXTENSION.fields_by_name['arguments'].message_type = _CPARGUMENT
_CPINTEGEREXPRESSION.fields_by_name['arguments'].message_type = _CPARGUMENT
_CPINTEGEREXPRESSION.fields_by_name['extensions'].message_type = _CPEXTENSION
_CPINTERVALVARIABLE.fields_by_name['arguments'].message_type = _CPARGUMENT
_CPSEQUENCEVARIABLE.fields_by_name['arguments'].message_type = _CPARGUMENT
_CPCONSTRAINT.fields_by_name['arguments'].message_type = _CPARGUMENT
_CPCONSTRAINT.fields_by_name['extensions'].message_type = _CPEXTENSION
_CPVARIABLEGROUP.fields_by_name['arguments'].message_type = _CPARGUMENT
_CPMODEL.fields_by_name['expressions'].message_type = _CPINTEGEREXPRESSION
_CPMODEL.fields_by_name['intervals'].message_type = _CPINTERVALVARIABLE
_CPMODEL.fields_by_name['sequences'].message_type = _CPSEQUENCEVARIABLE
_CPMODEL.fields_by_name['constraints'].message_type = _CPCONSTRAINT
_CPMODEL.fields_by_name['objective'].message_type = _CPOBJECTIVE
_CPMODEL.fields_by_name['search_limit'].message_type = ortools_dot_constraint__solver_dot_search__limit__pb2._SEARCHLIMITPARAMETERS
_CPMODEL.fields_by_name['variable_groups'].message_type = _CPVARIABLEGROUP
DESCRIPTOR.message_types_by_name['CpIntegerMatrix'] = _CPINTEGERMATRIX
DESCRIPTOR.message_types_by_name['CpArgument'] = _CPARGUMENT
DESCRIPTOR.message_types_by_name['CpExtension'] = _CPEXTENSION
DESCRIPTOR.message_types_by_name['CpIntegerExpression'] = _CPINTEGEREXPRESSION
DESCRIPTOR.message_types_by_name['CpIntervalVariable'] = _CPINTERVALVARIABLE
DESCRIPTOR.message_types_by_name['CpSequenceVariable'] = _CPSEQUENCEVARIABLE
DESCRIPTOR.message_types_by_name['CpConstraint'] = _CPCONSTRAINT
DESCRIPTOR.message_types_by_name['CpObjective'] = _CPOBJECTIVE
DESCRIPTOR.message_types_by_name['CpVariableGroup'] = _CPVARIABLEGROUP
DESCRIPTOR.message_types_by_name['CpModel'] = _CPMODEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CpIntegerMatrix = _reflection.GeneratedProtocolMessageType('CpIntegerMatrix', (_message.Message,), dict(
  DESCRIPTOR = _CPINTEGERMATRIX,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpIntegerMatrix)
  ))
_sym_db.RegisterMessage(CpIntegerMatrix)

CpArgument = _reflection.GeneratedProtocolMessageType('CpArgument', (_message.Message,), dict(
  DESCRIPTOR = _CPARGUMENT,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpArgument)
  ))
_sym_db.RegisterMessage(CpArgument)

CpExtension = _reflection.GeneratedProtocolMessageType('CpExtension', (_message.Message,), dict(
  DESCRIPTOR = _CPEXTENSION,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpExtension)
  ))
_sym_db.RegisterMessage(CpExtension)

CpIntegerExpression = _reflection.GeneratedProtocolMessageType('CpIntegerExpression', (_message.Message,), dict(
  DESCRIPTOR = _CPINTEGEREXPRESSION,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpIntegerExpression)
  ))
_sym_db.RegisterMessage(CpIntegerExpression)

CpIntervalVariable = _reflection.GeneratedProtocolMessageType('CpIntervalVariable', (_message.Message,), dict(
  DESCRIPTOR = _CPINTERVALVARIABLE,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpIntervalVariable)
  ))
_sym_db.RegisterMessage(CpIntervalVariable)

CpSequenceVariable = _reflection.GeneratedProtocolMessageType('CpSequenceVariable', (_message.Message,), dict(
  DESCRIPTOR = _CPSEQUENCEVARIABLE,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpSequenceVariable)
  ))
_sym_db.RegisterMessage(CpSequenceVariable)

CpConstraint = _reflection.GeneratedProtocolMessageType('CpConstraint', (_message.Message,), dict(
  DESCRIPTOR = _CPCONSTRAINT,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpConstraint)
  ))
_sym_db.RegisterMessage(CpConstraint)

CpObjective = _reflection.GeneratedProtocolMessageType('CpObjective', (_message.Message,), dict(
  DESCRIPTOR = _CPOBJECTIVE,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpObjective)
  ))
_sym_db.RegisterMessage(CpObjective)

CpVariableGroup = _reflection.GeneratedProtocolMessageType('CpVariableGroup', (_message.Message,), dict(
  DESCRIPTOR = _CPVARIABLEGROUP,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpVariableGroup)
  ))
_sym_db.RegisterMessage(CpVariableGroup)

CpModel = _reflection.GeneratedProtocolMessageType('CpModel', (_message.Message,), dict(
  DESCRIPTOR = _CPMODEL,
  __module__ = 'ortools.constraint_solver.model_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.CpModel)
  ))
_sym_db.RegisterMessage(CpModel)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
