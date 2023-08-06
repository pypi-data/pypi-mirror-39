# Copyright (C) 2010-2018 by Dr. Dieter Maurer <dieter@handshake.de>
"""Constructor factories.

Factories to generate add form and add action, usually used
as 'contructors' in the 'registerClass' call during Product
initialization.

These factories expect 'OFS.PropertyManager.PropertyManager' subclasses.
"""

from inspect import getargspec

from Products.PageTemplates.PageTemplateFile import PageTemplateFile



def add_form_factory(class_, action=None, description=None, charset=None, template=None, cname=None):
  """generate an add form for *class_*.

  *class_* must be a subclass of 'OFS.PropertyManager.PropertyManager'.

  *action* specifies the form action, it defaults to 'add_'
  followed by *cname*.

  *description* specifies a descriptive text which should help the
  user to understand the object he is about to create. It defaults
  to the class' docstring. Note that if not unicode, this will
  be converted by the template standard mechanism into unicode.

  *charset* specifies the charset used by the non unicode properties.
  If not specified, it is determined by searching 'management_page_charset'
  in the current environment and defaulting to 
  ZPublisher's default encoding.

  *template* is the page template
  that should be used for the generation of the form's HTML code.
  It is rendered with the keyword parameters 'charset', 'meta_type',
  'description', 'action', 'properties', 'class_' and 'cname'.
  It defaults to the package's 'generic_add_form'.
  Look at its code when you plan to customize the template.

  *cname* specifies the class name. It is used as part of the
  name of the generated function and as part of a CSS class
  and must adhere to the corresponding syntactic restrictions.
  It defaults to *class_*.__name__.
  """

  if cname is None: cname = class_.__name__
  if action is None: action = 'add_' + cname
  if description is None: description = class_.__doc__
  if template is None: template = add_form_template

  def add_form(self):
    """generated add form."""
    # determine charset for non unicode properties
    effective_charset = _get_effective_charset(self, charset)
    # note: we do not (yet) support read only properties
    properties = [p for p in getattr(class_, '_properties', ())
                  if 'w' in p.get('mode', 'rwd')
                  ]
    properties = _process_properties(properties, class_, effective_charset)
    return template.__of__(self)(
      charset=effective_charset,
      meta_type=class_.meta_type,
      description=description,
      action=action,
      properties=properties,
      class_=class_,
      cname=cname,
      )

  add_form.__name__ = 'add_%s_form' + cname

  return add_form


def add_action_factory(class_, hook=None, cname=None):
  """create add action for *class_*.

  *cname* specifies the class name. It is used as part of the
  name of the generated function
  and must adhere to the corresponding syntactic restrictions.
  It defaults to *class_*.__name__.

  The generated add action creates an instance of *class_*,
  sets its properties, adds it to the action's *self*, optionally
  calls *hook* on it and then either returns the acquisition wrapped
  instance or redirects to its management interface.

  The action is generated with the parameters 'self', 'id', 'props'
  and 'REQUEST'. 'props' and 'REQUEST' are optional. If 'props' is
  not given but 'REQUEST', it defaults to 'REQUEST.form'.

  *props* specifies property values for the created instance. If specified,
  it must be a mapping. If it contains values for unknown properties,
  they are silently ignored.

  If *REQUEST* is given, the action performs a redirect; otherwise,
  it returns the created instance.
  """
  if cname is None: cname = class_.__name__
  # try to find out whether the class requires an 'id' parameter for
  #  its constructor.
  #  Note: this check is not fully reliable. An explicit parameter might be necessary
  ci = class_.__init__
  pass_id = hasattr(ci, '__func__') and 'id' in getargspec(ci.__func__)[0]

  def add_action(self, id, props=None, REQUEST=None):
    """generated add action."""
    if pass_id: instance = class_(id)
    else: instance = class_(); instance._setId(id)
    id = instance.getId() # if the class defines the id
    if props is None and REQUEST is not None:
      props = _properties_from_request(self, instance, REQUEST.form)
    else: props = {}
    instance.manage_changeProperties(**props)
    id = self._setObject(id, instance) # if '_setObject' modifies the id
    wrapped = self._getOb(id)
    if hook is not None: hook(wrapped)
    if REQUEST is None: return wrapped
    REQUEST.response.redirect('%s/manage_workspace' % wrapped.absolute_url())

  add_action.__name__ = 'add_' + cname

  return add_action


def _get_effective_charset(self, charset):
  """determine the charset to be used for 'str' based values.

  If not specified explicitly, we look for
  'management_page_charset' in the acquisition containment
  and fall back to 'ZPublisher.HTTPResponse.default_encoding'.
  """
  def get_context():
    context = getattr(getattr(self, '_setObject', None), '__self__', None)
    if context is not None: context = self
    return context

  if charset is None:
    # try to determine 'management_page_charset'
    context = get_context()
    if hasattr(context, 'aq_acquire'):
      charset = context.aq_acquire(
        'management_page_charset', default=None, containment=True,
        )
    else: charset = getattr(self, 'management_page_charset', None)
  if charset is None:
    from ZPublisher.HTTPResponse import default_encoding
    charset = default_encoding
  if callable(charset): charset = charset(get_context())
  return charset


_ut = type(u"") # compatibility
_bt = type(b"") # compatibility

def _process_properties(props, class_, charset):
  """preprocess properties *props*.

  Preprocessing adds 'value', 'converted_value', 'control_value_type',
  'control_type' and (if necessary) 'type', 'description' and 'label' and
  for selections 'options' to the property definitions.

  Values are determined from *class_'.
  'converted_value' for string based properties are converted to unicode
  using *charset*. Tuples are resolved into a whitespace separated
  string with type specific whitespace separation.

  'control_value_type' is a ZPublisher type specification,
  'control_type' specifies the form control to be used.
  """
  def to_unicode(v):
    if v is None: return v
    if isinstance(v, _ut): return v
    if isinstance(v, _bt): return v.decode(charset)
    if isinstance(v, (list, tuple)): return tuple(map(to_unicode, v))
    v = str(v)
    return v if ininstance(v, ut) else v.decode(charset)
    
  lp = []
  for p in props:
    __traceback_info__ = p
    p = p.copy()
    pid = p['id']
    converted_value = p['value'] = getattr(class_, pid)
    control_type = 'input'
    control_value_type = ':utf8'
    convert = True
    type = p['type'] = p.get('type', 'string')
    p['label'] = p.get('label', pid)
    p['description'] = p.get('description', '')
    if type in ('int', 'float', 'long', 'date', 'boolean',):
      control_value_type = ':' + type; convert = False
      if type == 'boolean': control_type = 'checkbox'
    elif type in ('selection', 'multiple selection'):
      control_type = type
      control_value_type += ':ustring'
      multiple = type.startswith('multiple')
      if not multiple: converted_value = converted_value,
      else: control_value_type += ':list'
      options = getattr(class_, p['select_variable'])
      if callable(options): options = options()
      p['options'] = to_unicode(options)
    elif type in ('tokens', 'utokens'):
      control_value_type += ':utokens'
      converted_value = ' '.join(converted_value)
    elif type in ('lines', 'ulines'):
      control_value_type += ':ulines'
      converted_value = '\n'.join(converted_value)
      control_type = 'textarea'
    elif type in ('text', 'utext'):
      control_value_type += ':ustring'
      control_type = 'textarea'
    elif type in ('string', 'ustring'):
      control_value_type += ':ustring'
    else:
      # type unknown. Hope the default succeeds
      control_value_type = type; convert = False
    if convert: converted_value = to_unicode(converted_value)
    p['converted_value'] = converted_value
    p['control_type'] = control_type
    p['control_value_type'] = control_value_type
    lp.append(p)
  return lp


def _properties_from_request(self, obj, form):
  """determine a properties dict from *form*.

  Convert 'unicode' back to 'str' for 'str' based properties,
  using either a form supplied 'str_properties_charset_' variable
  or the effective charset found in the environment.
  """
  charset = _get_effective_charset(self, form.get('str_properties_charset_'))

  def to_str(v):
    if str is _ut: return v # `str` and `unicode` are the same
    if isinstance(v, _ut): return v.encode(charset)
    if isinstance(v, (list, tuple)): return map(to_str, v)
    return v

  props = {}
  for p in obj._properties:
    pid = p['id']
    v = form.get(pid)
    # handle missing value
    if v is None: continue
    ptype = p.get('type', 'string')
    # convert 'str' based properties
    if ptype in ('string', 'text', 'tokens', 'lines', 'selection', 'multiple selection',):
      v = to_str(v)
    props[pid] = v
  return props



# determine Zope major version -- necessary to choose the proper
#   template
try:
  from App.version_txt import getZopeVersion
  zope_major_version = getZopeVersion()[0]
except ImportError: zope_major_version = 4 # workaround for Zope 4 beta bug
add_form_template = PageTemplateFile(
  'generic_add_form' + ("-4" if zope_major_version >= 4 else ""),
  globals()
  )

