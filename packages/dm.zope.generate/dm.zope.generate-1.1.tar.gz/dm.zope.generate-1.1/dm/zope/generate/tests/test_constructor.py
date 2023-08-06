# Copyright (C) 2010 by Dr. Dieter Maurer <dieter@handshake.de>
# -*- coding: utf-8 -*-
"""'constructor' tests."""

from unittest import TestSuite, makeSuite
from urllib import urlencode
from StringIO import StringIO

from Testing.ZopeTestCase import installProduct, \
     ZopeTestCase, FunctionalTestCase
from OFS.Folder import Folder
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from DateTime import DateTime
from persistent import Persistent
from Acquisition import Implicit
from ZPublisher.HTTPResponse import default_encoding



installProduct('PythonScripts')
installProduct('PageTemplates')

from Products import PythonScripts
psm = PythonScripts._m


class _I(object):
  """auxiliary instance class."""
  def __init__(self, **kw): self.__dict__.update(kw)

class _C(SimpleItem, PropertyManager):
  """auxiliary content class."""


class UnitTests(ZopeTestCase):
  def test_get_effective_charset(self):
    from dm.zope.generate.constructor import _get_effective_charset as g
    # from "management_page_charset"
    #   unacquired
    o1 = Folder().__of__(self.app)
    o1.management_page_charset = 'mpc'
    self.assertEqual(g(o1, None), 'mpc')
    #   acquired
    o2 = Folder().__of__(o1)
    self.assertEqual(g(o2, None), 'mpc')
    #   skipping product dispatcher
    self.assertEqual(g(o2.manage_addProduct['PythonScripts'], None), 'mpc')
    # from ZPublisher
    del o1.management_page_charset
    self.assertEqual(g(o2, None), default_encoding)
    # explicit
    self.assertEqual(g(o2, 'explicit'), 'explicit')
    # explicit, callable
    o1.charset = 'ec'
    self.assertEqual(g(o2, lambda self: self.charset), 'ec')


class FunctionalTestLayer(object):
  @classmethod
  def setUp(cls_):
    from zope.component import provideAdapter
    from zope.interface import Interface
    from zope.traversing.adapters import DefaultTraversable
    provideAdapter(DefaultTraversable, (Interface,)) 

  @classmethod
  def tearDown(cls_):
    from zope.testing.cleanup import cleanUp
    cleanUp()


# the class definitions need to be outside because funtional tests
#  stupidly perform commits
class C1(_C):
      _properties = (
        dict(id='p_string',),
        dict(id='p_int', type='int',),
        dict(id='p_long', type='long',),
        dict(id='p_float', type='float',),
        dict(id='p_date', type='date',),
        dict(id='p_ustring', type='ustring',),
        dict(id='p_boolean', type='boolean',),
        dict(id='p_tokens', type='tokens',),
        dict(id='p_utokens', type='utokens',),
        dict(id='p_text', type='text',),
        dict(id='p_utext', type='utext',),
        dict(id='p_lines', type='lines',),
        dict(id='p_ulines', type='ulines',),
        dict(id='p_selection', type='selection', select_variable='s_options'),
        dict(id='p_ms', type='multiple selection', select_variable='ms_options'),
        dict(id='p_ms2', type='multiple selection', select_variable='ms_options'),
        )
      p_string = u'äöü'.encode(default_encoding)
      p_int = 1
      p_long = long(1)
      p_float = float(1)
      p_date = DateTime()
      p_ustring = u'äöü'
      p_boolean = True
      p_tokens = (p_string,)
      p_utokens = (p_ustring,)
      p_text = p_string
      p_utext = p_ustring
      p_lines = p_tokens
      p_ulines = p_utokens
      p_selection = 's1'
      p_ms = ('s1', 's3')
      p_ms2 = ('s1',)

      s_options = ('s1', 's2', 's3', 's4',)

      @classmethod
      def ms_options(cls_): return cls_.s_options


class C2(_C):
      _properties = (
        dict(id='p_boolean', type='boolean',),
        dict(id='p_ms', type='multiple selection', select_variable='ms_options'),
        )
      p_boolean = False
      p_ms = ()
      s_options = ('s1', 's2', 's3', 's4',)

      @classmethod
      def ms_options(cls_): return cls_.s_options


class FunctionalTests(FunctionalTestCase):
  layer = FunctionalTestLayer

  def test_all_properties(self):
    C = C1
    from dm.zope.generate.constructor import add_form_factory, add_action_factory
    app = self.app
    # emulate registration
    psm['add_C1'] = add_action_factory(C); psm['add_C__roles__'] = None
    post_data = self._parse(add_form_factory(C)(app))
    post_data['id'] = 'my_C'
    rsp = self.publish('manage_addProduct/PythonScripts/add_C1',
                       request_method='POST',
                       stdin=StringIO(urlencode(post_data, True)),
                       )
    self.assertEqual(rsp.getStatus(), 302)
    i = app.my_C
    self._check_properties(C, i)
    self.assertEqual(type(C.p_tokens[0]), type(i.p_tokens[0]))
    self.assertEqual(type(C.p_utokens[0]), type(i.p_utokens[0]))
    self.assertEqual(type(C.p_lines[0]), type(i.p_lines[0]))
    self.assertEqual(type(C.p_ulines[0]), type(i.p_ulines[0]))

  def test_missing_value(self):
    C = C2
    from dm.zope.generate.constructor import add_form_factory, add_action_factory
    app = self.app
    # emulate registration
    psm['add_C2'] = add_action_factory(C); psm['add_C__roles__'] = None
    post_data = self._parse(add_form_factory(C)(app))
    post_data['id'] = 'my_C'
    rsp = self.publish('manage_addProduct/PythonScripts/add_C2',
                       request_method='POST',
                       stdin=StringIO(urlencode(post_data, True)),
                       )
    self.assertEqual(rsp.getStatus(), 302)
    self._check_properties(C, app.my_C)
    

  def _parse(self, form):
    """parse form into a dict of its form controls variables."""
    from zope.testing.formparser import FormParser, Input

    def get_value(c):
      """*c*\\ s value."""
      if isinstance(c, Input) and c.type=='checkbox':
        if not c.checked: return
        return c.value is None and 'on' or c.value
      return c.value

    forms = FormParser(form.encode('utf-8')).parse()
    pform = forms[0]
    return dict(i for i in ((k, get_value(pform[k])) for k in pform.keys())
                if i[1] is not None
                )

  def _check_properties(self, class_, inst):
    for p in class_._properties:
      pid = p['id']
      cv, iv = getattr(class_, pid), inst.__dict__[pid]
      self.assertEqual(cv, iv, 'value of ' + pid)
      self.assertEqual(type(cv), type(iv), 'type of ' + pid)
    

def test_suite():
  return TestSuite(map(makeSuite,
    (UnitTests, FunctionalTests,)
                        ))


