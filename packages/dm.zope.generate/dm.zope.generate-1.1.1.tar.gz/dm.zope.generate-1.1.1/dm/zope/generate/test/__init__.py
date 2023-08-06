# Copyright (C) 2018 by Dr. Dieter Maurer <dieter@handshake.de>
"""Resources to test the package.

You need a Zope [2 or 4] setup and must ensure that this directories
`configure.zcml` is activated during startup.
"""

from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from DateTime import DateTime

from dm.zope.generate.constructor import add_form_factory, add_action_factory

class TestGenerator(SimpleItem, PropertyManager):
  """An object to test `dm.zope.generate.constructor`."""

  meta_type = "TestGenerator"

  manage_options = PropertyManager.manage_options + SimpleItem.manage_options

  # our properties
  _properties = PropertyManager._properties + (
    dict(id="p_boolean", type="boolean"),
    dict(id="p_date", type="date"),
    dict(id="p_float", type="float"),
    dict(id="p_int", type="int"),
    dict(id="p_lines", type="lines"),
    dict(id="p_long", type="long"),
    dict(id="p_string", type="string"),
    dict(id="p_text", type="text"),
    dict(id="p_tokens", type="tokens"),
    dict(id="p_ulines", type="ulines"),
    dict(id="p_ustring", type="ustring"),
    dict(id="p_utext", type="utext"),
    dict(id="p_utokens", type="utokens"),
    dict(id="p_selection", type="selection", select_variable="options"),
    dict(id="p_mselection", type="multiple selection", select_variable="options"),
    dict(id="p_label", label="Label"),
    dict(id="p_description", description="Description"),
    )

  # their default values
  p_boolean = False
  p_date = DateTime()
  p_float = 1.0
  p_int = 1
  p_lines = ("l1", "l2")
  p_long = 1
  p_string = "str"
  p_text = "text"
  p_tokens = ("t1", "t2")
  p_ulines = (u"L1", u"L2")
  p_ustring = u"STR"
  p_utext = u"TEXT"
  p_utokens = (u"T1", u"T2")
  p_selection = "O3"
  p_mselection = ("O1", "O3")
  p_label = "label"
  p_description = "description"

  # select variable for our selections
  @staticmethod
  def options(): return ("O1", "O2", "O3")


def initialize(context):
  context.registerClass(
    TestGenerator,
    constructors=(add_form_factory(TestGenerator),
                  add_action_factory(TestGenerator),
                  ),
    )

