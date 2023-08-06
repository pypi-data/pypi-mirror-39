# Copyright (C) 2004-2018 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Eppelborn, Germany
# see "LICENSE.txt" for details

from types import FunctionType

# marker value representing required arguments
REQUIRED = object()

def rebindFunction(f, rebindDir=None,
                   funcName=None, funcDoc=None,
                   argRebindDir=None, propRebindDir=None,
                   nameRebindDir=None,
                   **rebinds):
  '''return a function derived from *f* with rebinds specified by *rebindDir* and/or *rebinds*.

  Use *funcName* as function name, instead of `f.func_name` as function
  name, if given.
  
  *argRebindDir* is a dictionary mapping function parameter names
  to defaults. You can use this to turn required parameters into optional
  ones (by providing a default value for them), to change their
  default values or to turn optional parameters into required ones.
  Note that Python requires that required arguments must preceed
  optional ones. A `ValueError` is raised when *argRebindDir* violates
  this restriction.
  Note: we only support simply named parameters (not constructor expressions).

  *propRebindDir* is a dictionary specifying rebinds for the
  functions properties.

  *nameRebindDir* is a dictionary to specify renaming of variables used
  by the function code. It can be used to change local imports or
  references to global variables.

  ATT: *f.func_globals* is copied at rebind time. Later modifications
  may affect *f* but not the rebind function.

  Note: we would like to rebind closure parts as well but Python currently
  does not allow to create `cell` instances. Thus, this would be difficult.
  '''
  # unwrap a method
  f = getattr(f, '__func__', f)
  # handle global variable rebinds
  fg = f.__globals__.copy()
  if rebindDir: fg.update(rebindDir)
  if rebinds: fg.update(rebinds)
  # handle argument (default) rebinds
  if argRebindDir:
    args, _, _, defaults = getargspec(f)
    # ensure all arguments are known
    unknown = []
    for a in argRebindDir:
      if a not in args: unknown.append(a)
    if unknown:
      raise ValueError('unknown arguments in `argRebindDir`: %s'
                       % ', '.join(unknown)
                       )
    # determine new defaults
    defaults = defaults is not None and list(defaults) or []
    defaults = [REQUIRED] * (len(args) - len(defaults)) + defaults
    funcDefaults = []
    for (a,d) in zip(args, defaults):
      if isinstance(a, str) and a in argRebindDir: d = argRebindDir[a]
      if d is not REQUIRED: funcDefaults.append(d)
      elif funcDefaults: raise ValueError('required argument after optional one: %s' % a)
    funcDefaults = tuple(funcDefaults)
  else: funcDefaults = f.__defaults__ or ()
  if nameRebindDir:
    fc = f.__code__
    code = type(fc)(*(attr for attr in (
      fc.co_argcount, 
      getattr(fc, "co_kwonlyargcount", OMIT),
      fc.co_nlocals, fc.co_stacksize, fc.co_flags, fc.co_code,
      fc.co_consts, 
      tuple(nameRebindDir.get(n, n) for n in fc.co_names),
      # not sure rebinding "varnames" is a good thing
      tuple(nameRebindDir.get(n, n) for n in fc.co_varnames),
      fc.co_filename, fc.co_name, fc.co_firstlineno, fc.co_lnotab,
      fc.co_freevars, fc.co_cellvars,
      ) if attr is not OMIT)
      )
  else: code = f.__code__

  # construct the new function
  nf = FunctionType(
    code,
    fg, # func_globals
    funcName or f.__name__,
    funcDefaults,
    f.__closure__,
    )
  # handle the documentation
  if funcDoc is not None: nf.__doc__ = funcDoc
  else: nf.func_doc = f.__doc__
  # handle is properties
  if f.__dict__ is not None: nf.__dict__ = f.__dict__.copy()
  if propRebindDir:
    if nf.__dict__ is None: nf.__dict__ = {}
    nf.__dict__.update(propRebindDir)
  return nf


# Python version dependencies
OMIT = object()
try:
  from inspect import getfullargspec

  def getargspec(func):
    r = getfullargspec(func)
    if r.kwonlyargs or r.annotations:
      raise NotImplementedError("keyword-only args and annotations are not yet supported")
    return r[:4]
except ImportError:
  from inspect import getargspec
