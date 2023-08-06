# Copyright (C) 2018 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Eppelborn, Germany
# see "LICENSE.txt" for details
from inspect import getmembers, \
     ismethoddescriptor, isdatadescriptor, isfunction, ismethod
from types import MethodType


class OverridingProxy(object):
  """a proxy base class.

  Its instances behave almost like the proxied object
  but attributes and methods defined on the proxy override
  those of the proxied method.
  """
  _wrapped = None

  def __init__(self, *args, **kw):
    """return proxy for *obj* overriding attributes given by *kw*.

    The true signature for this method is `obj, **kw`.
    We have the more general signature because the call might in fact
    mean the `__init__` of the proxied object.
    """
    if self._wrapped is not None:
      return self.call_proxied_method("__init__", *args, **kw)
    obj, = args
    self.set_proxy_attribute("_wrapped", obj)
    for k in kw:
      self.set_proxy_attribute(k, kw[k])

  # official API
  def get_proxied_object(self): return self._wrapped

  def set_proxy_attribute(self, k, v):
    super(OverridingProxy, self).__getattribute__("__dict__")[k] = v

  def call_proxied_method(self, method, *args, **kw):
    """call the method *method* of the proxied object.

    This is used to be able to call on overridden method from
    the overriding method. The overridden method is called with
    the proxy as its `self`, not the proxied object.
    """
    m = getattr(self._wrapped, method)
    return self._rebind_proxied_method(m)(*args, **kw)


  ####################################################################
  ## configuration

  # which attributes should not get overridden
  delegated_attributes = frozenset((
    "__class__",  "__doc__", "__format__", "__hash__",
             "__repr__", "__str__", "__dict__",
    ))

  # which methods should not get proxied
  unproxied_methods = frozenset((
    "__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__",
    "__hash__",
    ))
    

  ####################################################################
  ## implementation
  def __getattribute__(self, k):
    if k in super(OverridingProxy, self).__getattribute__("delegated_attributes"):
      raise AttributeError(k) # let "__getattr__" take over
    # let proxy attributes override those of the proxied object
    return super(OverridingProxy, self).__getattribute__(k)

  def __getattr__(self, k):
    # activated, when `__getattribute__` raises `AttributeError`
    v = getattr(self._wrapped, k)
    return v if k in self.unproxied_methods else self._rebind_proxied_method(v)

  def __setattr__(self, k, v): setattr(self._wrapped, k, v)
  def __delattr__(self, k): delattr(self._wrapped, k)

  def __eq__(self, other):
    w_self = self._wrapped
    w_other = other.get_proxied_object() \
              if hasattr(other, "get_proxied_object") \
              else other
    return w_self == w_other

  def __ne__(self, other):
    w_self = self._wrapped
    if hasattr(w_self, "__ne__"):
      w_other = other.get_proxied_object() \
                if hasattr(other, "get_proxied_object") \
                else other
      return w_self != w_other
    return not (self == other)
  
  def _rebind_proxied_method(self, m):
    return (
      m.__class__(m.__func__, self) if isinstance(m, MethodType) and m.__self__ is not None
      else m
  )


_proxy_class_cache = {}

def _special_member(m):
  return ismethoddescriptor(m) or isdatadescriptor(m) or isfunction(m) or ismethod


def make_proxy(obj, proxy_class=OverridingProxy, unproxied_methods = None, **kw):
  """return a proxy of *obj* with overriding attributes specified by *kw*.

  *unproxied_methods* iterates over the names of methods which
  should be called with the the proxied object rather then the proxy
  as its `self`. If `None`, the corresponding attribute of *proxy_class*
  is used.
  """
  t = type(obj)
  assert not issubclass(t, OverridingProxy), "cannot proxy a proxy"
  if unproxied_methods is not None and not isinstance(unproxied_methods, frozenset):
    unproxied_methods = frozenset(unproxied_methods)
  key = proxy_class, t, unproxied_methods
  cls = _proxy_class_cache.get(key)
  if cls is None:
    delegates = proxy_class.delegated_attributes
    # determine overrides
    pm = dict(getmembers(proxy_class, _special_member))
    om = dict(getmembers(object, _special_member))
    overrides = set(k for k in pm
                    if pm[k] is not om.get(k) and k not in delegates
                    )
    cd = {}
    for k, d in getmembers(t, _special_member):
      if k in overrides: continue
      delegator = \
          _Delegator if k.startswith("__") and k.endswith("__") and  (
                        ismethoddescriptor(d) or isfunction(d) or ismethod(d)
                        )\
          else _MethodDescriptorDelegator if ismethoddescriptor(d) \
          else _DataDescriptorDelegator if isdatadescriptor(d) \
          else None
      if delegator is None: continue
      cd[k] = delegator(k, d)
    if unproxied_methods is not None:
      cd["unproxied_methods"] = unproxied_methods
    cls = _proxy_class_cache[key] = \
          type(proxy_class.__name__, (proxy_class,), cd) if cd else proxy_class
  return cls(obj, **kw)


class _Delegator(object):
  """Auxiliary class to delegate special methods"""
  def __init__(self, name, unused): self._name = name

  def __call__(self, proxy, *args):
    name = self._name
    if name in proxy.unproxied_methods:
      return getattr(proxy._wrapped, name)(*(
        a.get_proxied_object() if hasattr(a, "get_proxied_object") else a
        ))
    return proxy.call_proxied_method(name, *args)

  def __get__(self, proxy, owner):
    return self if proxy is None else lambda *args: self(proxy, *args)

class _MethodDescriptorDelegator(object):
  """Auxiliary class to delegate method descriptors."""
  def __init__(self, name, target): self._name = name; self._target = target

  def __get__(self, proxy, owner):
    if proxy is None: return self
    name = self._name
    obj = proxy.get_proxied_object() if name in proxy.unproxied_methods else proxy
    return self._target.__get__(obj, proxy.__class__)

class _DataDescriptorDelegator(_MethodDescriptorDelegator):
  """Auxiliary class to delegate data descriptors."""
  def __set__(self, proxy, value): self._traget.__set__(proxy, value)
  def __delete__(self, proxy): self._target.__delete__(proxy)
