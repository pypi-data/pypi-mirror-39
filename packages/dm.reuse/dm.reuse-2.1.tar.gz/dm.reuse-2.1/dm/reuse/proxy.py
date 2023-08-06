# Copyright (C) 2018 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Eppelborn, Germany
# see "LICENSE.txt" for details
from types import MethodType


class OverridingProxy(object):
  """a proxy base class.

  Its instances behave almost like the proxied object
  but attributes and methods defined on the proxy override
  those of the proxied method.
  """
  _wrapped = None

  def __init__(self, obj, **kw):
    """return proxy for *obj* overriding attributes given by *kw*."""
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



  # implementation
  def __getattribute__(self, k):
    if k in ("__class__", "__delattr__", "__doc__", "__format__", "__hash__",
             "__repr__", "__setattr__", "__str__", "__dict__"):
      return getattr(self._wrapped, "k")
    # let proxy attributes override those of the proxied object
    return super(OverridingProxy, self).__getattribute__(k)

  def __getattr__(self, k):
    # activated, when `__getattribute__` raises `AttributeError`
    v = getattr(self._wrapped, k)
    return v if not (isinstance(v, MethodType) and v.__self__ is not None) \
           else self._rebind_proxied_method(v)

  def __setattr__(self, k, v): setattr(self._wrapped, k, v)
  def __delattr__(self, k): delattr(self._wrapped, k)
  
  def _rebind_proxied_method(self, m):
    assert isinstance(m, MethodType)
    return m.__class__(m.__func__, self)


def make_proxy(obj, proxy_class=OverridingProxy, **kw):
  """return a proxy of *obj* with overriding attributes specified by *kw*."""
  return proxy_class(obj, **kw)
