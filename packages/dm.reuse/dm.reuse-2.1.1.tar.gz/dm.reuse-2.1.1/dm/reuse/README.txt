dm.reuse
========

Utilities to reuse (slightly modified) objects in new contexts.

Currently, there is are two utilities: ``rebindFunction`` and
``OverridingProxy``.

``rebindFunction``
++++++++++++++++++

``rebindFunction`` allows to reuse the code of a function while changing
name, globals, default arguments, properties and/or names used.

Lets look at a trivial example. Function ``f`` accesses global variables
``i`` and ``j``.

Examples
--------

>>> i = 1; j = 2
>>> def f(): return i, j
...
>>> f()
(1, 2)

We want to derive a new function `g` which binds `i` to `-1`:

>>> from dm.reuse import rebindFunction
>>> g=rebindFunction(f, i=-1)
>>> g()
(-1, 2)

We can specify the rebinds not only via keyword arguments but via
a dictionary as well:

>>> g=rebindFunction(f, dict(i=-1, j=-2))
>>> g()
(-1, -2)

Usually, the function name is taken over from the original function,
but it can be changed:

>>> f.__name__
'f'
>>> g.__name__
'f'
>>> g=rebindFunction(f, dict(i=-1, j=-2), funcName='g')
>>> g.__name__
'g'
>>> g()
(-1, -2)

The originals function docstring is taken over, too -- unless
overridden:

>>> f.func_doc = 'some documentation'
>>> g=rebindFunction(f, dict(i=-1, j=-2))
>>> f.__doc__ is g.__doc__
True
>>> g=rebindFunction(f, dict(i=-1, j=-2), funcDoc='some new documentation')
>>> g.__doc__
'some new documentation'

Default values for arguments can be added, removed or changed.
Unknown arguments are recognized:

>>> def f(a1, a2=2): return a1, a2
...
>>> g=rebindFunction(f, argRebindDir=dict(a1=1))
>>> g()
(1, 2)

>>> from dm.reuse import REQUIRED
>>> g=rebindFunction(f, argRebindDir=dict(a2=REQUIRED))
>>> g(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
  ...
TypeError: f() takes exactly 2 arguments (1 given)

>>> g=rebindFunction(f, argRebindDir=dict(a2=10))
>>> g(1)
(1, 10)

>>> g=rebindFunction(f, argRebindDir=dict(a3=10))
Traceback (most recent call last):
  ...
ValueError: unknown arguments in `argRebindDir`: a3

Finally, function properties can be rebound with `propRebindDir`.
We are careful, to give the new function a separate new property dict.

>>> f.prop='p'
>>> g=rebindFunction(f)
>>> g.prop
'p'
>>> g=rebindFunction(f, propRebindDir=dict(prop='P', prop2='p2'))
>>> g.prop, g.prop2
('P', 'p2')
>>> f.__dict__
{'prop': 'p'}

Occationally, functions use local imports which are not adequate
in the new context. In order to provide control over them, names
used inside the function code can be changed.

>>> def f(a): import codecs; return codecs, a
...
>>> g=rebindFunction(f, nameRebindDir=dict(codecs='urllib'))
>>> r = g(1)
>>> r[0].__name__, r[1]
('urllib', 1)

This way, references to global variables can be changed as well.

>>> i1, i2 = 1, 2
>>> def f(): return i1
... 
>>> g=rebindFunction(f, nameRebindDir=dict(i1='i2'))
>>> g()
2


``OverridingProxy``
+++++++++++++++++++

Occasionally, you must work with an object, whose overall functionality
is mostly adequate but small aspects need to be changed.
In those cases, ``OverridingProxy`` might be of help. It allows
to proxy an object. The proxy mostly behaves like the proxied
object but some attributes/methods are overridden.

Examples
--------

We set up a play object ``c`` and pretend that we must use it
with modified attribute ``attr1``. We achieve this with a proxy
which behaves almost like ``c`` but has the attribute changed.

>>> from dm.reuse.proxy import OverridingProxy, make_proxy
>>> 
>>> class C(object):
...   attr1 = 1
...   attr2 = 2
...   def f(self): return self.attr1, self.attr2
...   def g(self): return self.f()
... 
>>> c = C()
>>> p = make_proxy(c, attr1='overridden attr1')
>>> p.__class__ is C
True
>>> isinstance(p, C)
True
>>> p.attr1
'overridden attr1'

The change is also effective when we call methods which use
the overrriden attribute.

>>> p.f()
('overridden attr1', 2)

If we assign a new value to a proxy attribute, then the
corresponding attribute on the proxied object is changed.
As a consequence, changing overridden attributes have
apparently no effect -- this is unintuitive and might be changed
in the future.

>>> p.attr2 = "new attr2"
>>> p.f()
('overridden attr1', 'new attr2')
>>> p.attr1 = "new attr1"
>>> c.attr1
'new attr1'
>>> p.f()
('overridden attr1', 'new attr2')

You can use the method ``set_proxy_attribute`` to change
the proxies attributes rather than those of the proxied method.

>>> p.set_proxy_attribute("attr1", "new overridden attr1")
>>> p.f()
('new overridden attr1', 'new attr2')

A proxy compares usually equal to its proxied object. Sometimes,
this works also for the inverse. But, two
proxies for the same proxied object compare usually equal.

>>> p == c
True
>>> c == p
True
>>> make_proxy(c) == p
True


Usually, you would not override simple attributes but methods.
This is easier to achieve with a custom proxy class.
In many cases, an overriding method will want to call the
overridden method; this is possible via ``call_proxied_method``.

>>> class MyProxy(OverridingProxy):
...   def g(self):
...     print ("g called")
...     return self.call_proxied_method("g")
... 
>>> p = make_proxy(c, MyProxy, attr1="overridden attr1")
>>> p.g()
g called
('overridden attr1', 'new attr2')


The proxies have limited support for special methods and
thereby support e.g. subscription. Note that this support
is incomplete and surprises are possible.

>>> class MyDict(dict, C): pass
...
>>> md = MyDict(dict(a=1, b=2))
>>> p = make_proxy(md, attr1="overridden attr1")
>>> p.f()
('overridden attr1', 2)
>>> p["a"]
1
>>> class MySequence(C):
...   seq = 0, 1, 2
...   def __getitem__(self, i): return self.seq[i]
...
>>> c = MySequence()
>>> p = make_proxy(c, seq=(10, 11, 12))
>>> p[0]
10
>>> p = make_proxy(c)
>>> p[0]
0


Usually, descriptors, too, see the modified state.

>>> class WithProperty(C):
...   @property
...   def attr1_prop(self): return self.attr1
...
>>> c = WithProperty()
>>> p = make_proxy(c, attr1="overridden attr1")
>>> p.attr1_prop
'overridden attr1'


History
+++++++

2.1
  added ``OverridingProxy``, allowing to reuse objects with
  small modifications

2.0
  added partial support for Python 3 (keyword only arguments and
  annotations are not yet supported)

  dropped support for Python before 2.7

1.1
  ``nameRebindDir`` support added
