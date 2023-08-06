import re
import sys
from collections import defaultdict
from pathlib import Path
import inspect
import argparse
from typing import List, Optional, Dict, Callable, Any, Tuple, Set, get_type_hints, GenericMeta, Iterable, Sequence, Union

Converter = Callable[[str], Any]
Converters = Dict[object, Converter]
GeneralFunc = Callable[..., Any]
# Recursive types: https://github.com/python/mypy/issues/731
#Spec = Union[GeneralFunc, List[GeneralFunc], Tuple[GeneralFunc], Set[GeneralFunc], Dict[str, 'Spec']]
Spec = Any

def main(spec: Spec = None) -> None:
	if spec is None:
		spec = inspect.stack()[1][0].f_globals.get('main')
		if spec is None:
			raise KeyError("'main' function not defined")
		if not callable(spec):
			raise TypeError("'main' must be callable")
	sys.exit(run(spec))

def run(spec: Spec, args: Optional[List[str]] = None, *, converters: Optional[Converters] = None) -> Any:
	if args is None:
		args = sys.argv[1:]
	convs = dict(CONVERTERS)
	if converters is not None:
		convs.update(converters)
	parser = argparse.ArgumentParser()
	spec_to_argparse(spec, parser, convs)
	ns = parser.parse_args(args)
	if not hasattr(ns, '_func'):
		parser.print_help()
		sys.exit(0)
	callable = ns._func
	post = ns._post
	args, kwargs = extract_args(callable, ns, post)
	return callable(*args, **kwargs)

def spec_to_argparse(spec: Spec, parser: argparse.ArgumentParser, converters: Converters) -> None:
	if isinstance(spec, dict):
		subparsers = parser.add_subparsers()
		for k, v in spec.items():
			spec_to_argparse(v, subparsers.add_parser(k), converters)
		return
	
	if isinstance(spec, (list, set, tuple)):
		subparsers = parser.add_subparsers()
		for f in spec:
			spec_to_argparse(f, subparsers.add_parser(f.__name__), converters)
		return
	
	argspec = inspect.getfullargspec(spec)
	annots = get_type_hints(spec)
	
	post = {} # type: Dict[str, Callable[[Any], Any]]
	parser.set_defaults(_func = spec, _post = post)
	
	defaults = argspec.defaults or ()
	j = len(argspec.args) - len(defaults)
	for i, arg in enumerate(argspec.args):
		required = (i < j)
		default = (None if required else defaults[i - j])
		container, content = decompose_annotation(annots.get(arg))
		dest = ('' if required else '--') + arg
		if required or content is not bool:
			if required:
				parser.add_argument(dest, default = default, type = get_converter(converters, content))
			else:
				# Typings for `nargs` are incorrect:
				# https://github.com/python/typeshed/blob/f9ba5402f8ec13485daa35da9292aa3cd02939f2/stdlib/2and3/argparse.pyi#L58
				parser.add_argument(dest, default = default, type = get_converter(converters, content), nargs = ('*' if container else None)) # type: ignore
				if container is not None:
					post[arg] = container
		else:
			parser.add_argument(dest, default = default, action = 'store_true')
	if argspec.varargs:
		converter = get_converter(converters, annots.get(argspec.varargs))
		parser.add_argument(argspec.varargs, type = converter, nargs = '*')
	
	kwonlydefaults = argspec.kwonlydefaults or {}
	for arg in argspec.kwonlyargs:
		required = (arg not in kwonlydefaults)
		default = kwonlydefaults.get(arg)
		container, content = decompose_annotation(annots.get(arg))
		dest = '--' + arg
		if required or content is not bool:
			# Typings for `nargs` are incorrect:
			# https://github.com/python/typeshed/blob/f9ba5402f8ec13485daa35da9292aa3cd02939f2/stdlib/2and3/argparse.pyi#L58
			parser.add_argument(dest, default = default, required = required, type = get_converter(converters, content), nargs = ('*' if container else None)) # type: ignore
			if container is not None:
				post[arg] = container
		else:
			parser.add_argument(dest, default = default, required = required, action = 'store_true')
	if argspec.varkw:
		# Not supported by argparse
		pass

def get_converter(converters: Converters, annot: Any) -> Converter:
	if annot is None: return str
	converter = converters.get(annot)
	if converter is None:
		raise KeyError("no converter available for {!r}".format(annot))
	return converter

def decompose_annotation(annot: Any) -> Tuple[Optional[type], Any]:
	annot = deoptionalize(annot)
	if annot is list: return decompose_annotation(List)
	if annot is set: return decompose_annotation(Set)
	if annot is tuple: return decompose_annotation(Tuple)
	if not isinstance(annot, GenericMeta):
		return None, annot
	origin = getattr(annot, '__origin__', None)
	args = getattr(annot, '__args__', None)
	if origin is None or not args:
		annot = (origin or annot)[Any] # type: ignore
		return decompose_annotation(annot)
	arg = deoptionalize(args[0])
	if origin in (Iterable, Sequence, List): return list, arg
	if origin is Set: return set, arg
	if origin is Tuple: return tuple, arg
	return None, annot

NoneType = type(None)

def deoptionalize(annot: Any) -> Any:
	if annot is Union: return Any
	origin = getattr(annot, '__origin__', None)
	if origin is Union:
		args = getattr(annot, '__args__', [])
		# Use of `NoneType` in next line is a false positive with MyPy:
		# https://github.com/python/mypy/issues/5354
		args = [a for a in args if a is not NoneType] # type: ignore
		if len(args) == 1:
			return deoptionalize(args[0])
	return annot

def extract_args(callable: GeneralFunc, ns: argparse.Namespace, post: Dict[str, Callable[[Any], Any]]) -> Tuple[List[Any], Dict[str, Any]]:
	args = []
	kwargs = {}
	
	def _convert_arg(arg: str) -> Any:
		value = getattr(ns, arg)
		if value is None: return None
		post_arg = post.get(arg)
		if post_arg is None: return value
		return post_arg(value)
	
	argspec = inspect.getfullargspec(callable)
	for arg in argspec.args:
		args.append(_convert_arg(arg))
	if argspec.varargs:
		args.extend(getattr(ns, argspec.varargs))
	for arg in argspec.kwonlyargs:
		kwargs[arg] = _convert_arg(arg)
	if argspec.varkw:
		kwargs.update(getattr(ns, argspec.varkw, {}))
	
	return args, kwargs

def parse_bool(s: str) -> bool:
	if s == 'True': return True
	if s == 'False': return False
	raise ValueError("invalid bool literal: {!r}".format(s))

CONVERTERS = {
	str: str,
	int: int,
	float: float,
	bool: parse_bool,
	Path: Path,
} # type: Converters
