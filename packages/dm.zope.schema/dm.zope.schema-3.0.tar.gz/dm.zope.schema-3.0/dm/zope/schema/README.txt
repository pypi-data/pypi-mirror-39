This package contains extensions for ``zope.schema``.

=======
Modules
=======

verify
======

A companion to ``zope.interface.verify`` for the schema part of
interfaces.

It contains the function
``verify_schema(``\ *iface*, *obj*, *context*\ ``=None``, *check_declaration*\ ``=True)``
which verifies that *obj* satisfies the schema part of interface *iface*.
Schema fields need to get bound to a context before they can be validated.
*context* specifies this context and defaults to *obj*.
*check_declaration* checks that *obj* declares to provide *iface*.

schema
======

The main content is the mixin class ``SchemaConfigured``. It supports
configuration according the schema part of the interfaces implemented
by the ``SchemaConfigured`` derived class. If you want to
control from which interfaces the schema is derived,
you can use the class attribute ``SC_SCHEMAS``: its value should be
``None`` (derive schema automatically from the implemented interfaces),
a single interface or a tuple of interfaces. Taking explicit control
over the interfaces used to determine the schema is especially important
for Zope 2 schema configured content classes (as their base
class ``OFS.SimpleItem.SimpleItem`` implements a huge number of
interfaces whose fields you likely do not want in your schema).

The mixin class ``SchemaConfiguredEvolution`` provides support
for schema evolution for (ZODB) persistent objects. Its ``__setstate__``
adds missing attributes to the object such that you can add new fields
to your schema and still find all corresponding attributes on the
respective objects even when those have been created before the extension.
Note: in order for ``SchemaConfiguredEvolution`` to be effective, it must
come early in the method resolution order (``mro``)
(before ``persistent.Persistent``).
That's why is is a separate class and its feature not included
in ``SchemaConfigured`` itself (there may be good reasons
to have ``SchemaConfigured`` late in the ``mro``).
As an alternative to the use of ``SchemaConfiguredEvolution``,
you can use default values defined on class level for new fields.

Occasionally, functions ``schemaitems`` and ``schemadict`` might be usefull.
They extract
the schema part of an interface or interface specification as
a list of id, field pairs or a dictionary, respectively.

The field ``Object`` is a replacement for ``zope.schema.Object``.
In former ``zope.schema`` versions, its ``Object``
lacked field information in validation errors
(https://bugs.launchpad.net/zope.schema/+bug/620324) which made identification
of the affected fields unnecessarily difficult; this package's ``Object``
was designed to work around this bug.
Modern ``zope.schema`` versions have fixed the bug and
this package's ``Object`` now behaves almost as that of ``zope.schema``.
However, it allows to suppress the check that the validated
object explicitely declares to provide the interface.
``Object`` has the additional
property ``check_declaration`` to control this (defaults to ``True``).


propertymanager
===============

This module implements a schema based ``OFS.PropertyManager.PropertyManager``
subclass. The ``_properties`` attribute describing the properties is
not maintained on the class or its instances but derived from
the provided (respectively implemented) schemas. For the moment,
properties cannot be extended on an instance based level (other than by
providing another schema).

``zope.schema`` uses unicode to represent text. ``PropertyManager``
can in principle support unicode properties. However, due to a
bug/weakness, the property management page handles them correctly
only, when ``management_page_charset`` is not defined or has
value ``UTF-8`` (note the upper case spelling!). We use unicode
properties by default unless ``management_page_charset.upper()`` yields
a value different from ``UTF-8``. We also provide a mixin class
``WorkaroundSpelling_management_page_charset`` to work around Zope's
stupid insistence on upper case spelling for ``management_page_charset``.

For the moment, the following field types are supported:
``Text``, ``TextLine``, ``Bytes``, ``BytesLine``, ``Bool``, ``Int``,
``Float`` and ``List`` with a value type of ``TextLine`` or ``BytesLine``.
Other types will raise ``NotImplementedError``.

The module has been implemented to leverage ``dm.zope.generate``.
An alternative would have been the implementation of the generation facilities
based on "zope.formlib" and the use of so called add forms. Depending
on experience, I may switch to this alternative.


form
====

The module defines default edit (``SchemaConfiguredEditForm``)
and display (``SchemaConfiguredDisplayForm``) forms for
``dm.zope.schema.schema.SchemaConfigured``.

It depends on ``zope.formlib``.


widget
======

Provides display and edit widgets for ``Timedelta`` fields,
a decent display widget for ``Password`` fields (the default
displays passwords in cleartext) and an input widget for ``Password``
that does not force you to provide the password value whenever you edit the form.

It depends on ``zope.app.form`` in older Zope versions and on
``zope.formlib`` in newer ones.


tag
===

Often you would like to provide additional information for your fields -
usually with effects to presentation. Unfortunately, ``zope.schema`` has
forgotten this use case: it is really hard to give existing fields
additional properties.

Fortunately, `zope.schema` is build on top of `zope.interface` and it
supports so called "tagged values" to add additional information to
its elements. This module uses this feature to provide additional information
for schema elements. As a matter of fact, it works for all schema elements,
not just fields.

Note: If your schemas are used across different packages, ensure the
tag names are sufficiently specific to avoid name clashes, e.g.
by using an appropriate prefix.


dataschema
==========

``zope.schema`` is nice to describe objects with attributes. But sometimes,
you would like to work with mappings whose keys are described by
a schema. This module contains auxiliary classes to bridge the gap
between (schema controlled) objects and (schema controlled) mappings.

``SchemaDict`` is a dictionary with keys described by a schema
and ``MappingBySchema`` is a mixin class to provide a (schema controlled)
mapping interface to an object.


z2
==

This subpackage combines schema related and
Zope2/Zope 4+ functionality. In newer Zope versions, it depends on
``five.formlib`` (and, of course, on Zope2 or Zope 4+, respectively).
Note that ``five.formlib`` was not yet Python 3 compatible when
this package has been released.


form
----

The module defines default edit (``SchemaConfiguredEditForm``)
and display (``SchemaConfiguredDisplayForm``) forms for
``dm.zope.schema.schema.SchemaConfigured`` for use in Zope2/Zope 4+.

It depends on ``zope.formlib``.



constructor
-----------

This module contains an add form class ``SchemaConfiguredAddForm``
and a factory ``add_form_factory``
for the generation of an add form (called "constructor" by Zope 2)
for ``dm.zope.schema.schema.SchemaConfigured`` based classes.
The generated add form is usually used as part of the ``constructors``
parameter to ``registerClass``.

``add_form_factory`` has the parameters:

  =============  ===========================             ======================================
  name           default                                 description
  =============  ===========================             ======================================
  *class_*                                               the class to generate the form for
  *title*        Create instance of *class_*             the title shown in the form
  *description*  *class_*\ ``.__doc__``                  the documentation shown in the form
  *form_class*   ``SchemaConfiguredAddForm``             form class to be used
  =============  ===========================             ======================================

``add_form_factory`` generates a ``zope.formlib`` form with fields
defined by the implemented schemas of
``dm.zope.schema.schema.SchemaConfigured`` class *class_*.


This module is similar to ``dm.zope.generate.constructor``. However,
it works for ``SchemaConfigured`` based classes while the latter
supports ``PropertyManager`` based classes.


template
--------

Provides the view page template ``form_template`` able to view and edit
Zope2/Zope 4+
schema configured content objects within the standard ZMI interface.



========
Examples
========

Setup: It defines two schemas ``S1`` and ``S2``, an
interface ``I`` and a class ``C`` deriving from ``SchemaConfigured``
implementing the schemas and the interface.

>>> from zope.interface import Interface, implementer, providedBy
>>> from zope.schema import Int
>>> 
>>> from dm.zope.schema.schema import SchemaConfigured
>>> from dm.zope.schema.verify import verify_schema
>>> 
>>> class S1(Interface): i1 = Int(default=0)
... 
>>> class S2(Interface): i2 = Int(default=1)
... 
>>> class I(Interface):
...   def method(): pass
... 
>>> @implementer(S1, S2, I)
... class C(SchemaConfigured):
...   def method(self): pass
... 


``C`` instances have attributes corresponding to the schema fields.
If no arguments are given for the constructor, they get the field default
as value. Provided (keyword!) arguments override the defaults.

>>> c = C()
>>> c.i1
0
>>> c.i2
1
>>> c = C(i1=5)
>>> c.i1
5

The constructor rejects keyword arguments not defined in the schema
in order to quickly detect spelling errors. However, this hampers
the use of ``super`` in the class hierarchy for the ``__init__`` method.
Maybe, future versions will provide a means to control this check.

>>> c = C(x=5)
Traceback (most recent call last):
  ...
TypeError: non schema keyword argument: x

If the field values are appropriate, ``C`` instances provide the
schemas (as verified by ``verify_schema``). Otherwise, ``verify_schema``
will raise an exception.

This example demonstrates also the elementary use
of ``verify_schema``. Note that ``verify_schema`` raises different
exceptions in case of failure depending on the version of ``zope.schema``
(``WrongContainedType`` in older version,
``SchemaNotCorrectlyImplemented`` in newer versions).

>>> verify_schema(S1, c)
>>> c.i1=None
>>> try: verify_schema(S1, c)
... except Exception as e: e.args[0]
[RequiredMissing('i1')]


We can also explicitely specify which schemas our class should
support via the class variable ``SC_SCHEMA``.

>>> class SC(SchemaConfigured):
...   SC_SCHEMAS = S1, S2
...
>>> sc = SC()
>>> sc.i1
0
>>> sc.i2
1
>>> verify_schema(S1, sc, check_declaration=False)



We can create an edit (or display) form for our objects. Form fields
are automatically created for our schema fields.
The form classes have a ``customize_fields`` method you can override
to provide custom fields and/or widgets.

Similar functionality is available for Zope 2/Zope 4 in the ``z2`` subpackage.

>>> from zope.publisher.browser import TestRequest
>>> from dm.zope.schema.form import SchemaConfiguredEditForm
>>>
>>> form = SchemaConfiguredEditForm(c, TestRequest())
>>> list([f.__name__ for f in form.form_fields])
['i1', 'i2']


Schemas describe a data model with properties relevant for either
documentation, validation or the user interface. Occasionally,
you may want to use a schema for other purposes as well --
and then, you may lack properties to satisfy the requirements.
I ran into this for ``dm.zope.reseller`` where I wanted to
use schemas to also partially describe data models
in a relational database. For this, I needed the concept
"informational field" describing a field not directly stored in
the database but computed from other database fields.
I used tagging as shown in the example below.

>>> from dm.zope.schema.tag import Tagger
>>> tag = Tagger("dm.zope.reseller")
>>> class S(Interface):
...   i1 = tag(Int(default=0), informational=True)
...   i2 = Int(default=1)
... 

We check for an informational field:

>>> tag.get(S["i1"], "informational")
True
>>> tag.get(S["i2"], "informational")

We can also ask which tags are available:

>>> tag.list(S["i1"])
['informational']

If we need to check for various tags on a field, we can wrap
it and then access the tags with typical mapping methods.

>>> te = tag.wrap(S["i1"])
>>> list(te)
['informational']
>>> te["informational"]
True
>>> "informational" in te
True
>>> te.unwrap() is S["i1"]
True



=======
History
=======

3.0

  Python3/Zope4 compatibility.
  Note that the subpackage ``z2`` depends on ``five.formlib``
  which was not yet Python 3 compatible when this version was
  released.

  Modern versions of ``zope.schema`` have removed a major weaknees
  of its ``Object`` field: its validation now registers for
  failing subfields the field name in the corresponding exception
  (usually in its `field` attribute). The ``Object`` field of this
  package has been changed in an incompatible way to match the
  ``zope.schema`` behaviour; its only difference is now that
  it allows to suppress the "provides" check.

  More examples and test resources.

2.1

  Modules ``tag`` and ``dataschema``

2.0

  form support

  Zope 2 constructor support
