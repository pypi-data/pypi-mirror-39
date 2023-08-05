"""Side effects as data todos."""


# [ Imports:Python ]
import contextlib
import copy
import inspect
import typing

# [ Imports:Third Party ]
import mypy_extensions


# XXX add testing for __all__/dir


# [ Internal ]
def _indent(string: str, *, indent: str) -> str:
    lines = string.splitlines()
    indented_lines = (f'{indent}{l}' for l in lines)
    indented = '\n'.join(indented_lines)
    return indented


def _iterable(thing: typing.Any) -> bool:
    try:
        iter(thing)
    except TypeError:
        return False
    else:
        return True


def _is_str(obj: typing.Any) -> bool:
    """Return whether obj is a string."""
    return isinstance(obj, str)


def _is_dict(obj: typing.Any) -> bool:
    """Return whether obj is a dictionary."""
    return isinstance(obj, dict)


def _is_normal_iterable(obj: typing.Any) -> bool:
    """Return whether obj is a non-string, non-dictionary, non-generator, iterable."""
    return _iterable(obj) and not inspect.isgenerator(obj) and not isinstance(obj, (str, dict))


def _is_custom_repr_obj(obj: typing.Any) -> bool:
    """Return whether obj has a custom repr not crafted by the repr_mixin."""
    if not isinstance(obj, ReprMixin):
        default_repr = repr(obj)
        if f'at {hex(id(obj))}' not in default_repr:
            return True
    return False


def _is_repr_mixin_obj(obj: typing.Any) -> bool:
    """Return whether obj is a repr_mixin."""
    return isinstance(obj, ReprMixin)


class _FormatCase(typing.NamedTuple):
    """Format case for formatting reprs for objects."""

    matches: typing.Callable[
        [typing.Any],
        bool,
    ]
    format_: typing.Callable[
        [
            typing.Any,
            mypy_extensions.NamedArg(str, 'indent'),
        ],
        str,
    ]


def _get_repr_attributes(obj: typing.Any) -> typing.Dict[str, typing.Any]:
    attribute_names = dir(obj)
    # public attrs
    public_attributes = (a for a in attribute_names if not a.startswith('_'))
    # non-methods
    non_self_bound = (a for a in public_attributes if getattr(getattr(obj, a), '__self__', None) != obj)
    # non-class/static-methods
    non_self_bound = (a for a in non_self_bound if not getattr(getattr(obj, a), '__qualname__', "").endswith(f"{obj.__class__.__name__}.{a}"))
    # standard id attrs
    standard_attrs = (a for a in ('__name__', '__qualname__', '__module__', '__file__') if getattr(obj, a, None))
    all_attrs = (*non_self_bound, *standard_attrs)
    # prefer __qualname__ to __name__
    if all(a in all_attrs for a in ('__name__', '__qualname__')):
        attr_list = list(all_attrs)
        attr_list.remove('__name__')
        all_attrs = tuple(attr_list)
    # Data to represent
    attributes = {k: getattr(obj, k) for k in all_attrs}

    return attributes


class _ReprFormatter:
    """A formatter for reprs."""

    def __init__(self) -> None:
        """Initialize the state."""
        self._repr_id_dict: typing.Dict[int, str] = {}

    def _format_attribute(self, name: str, *, value: typing.Any, indent: str) -> str:
        """Format a key/value pair item for a repr."""
        return f'{name}: {self.format_obj(value, indent=indent)}'

    def _format_pair(self, key: str, *, value: typing.Any, indent: str) -> str:
        """Format a key/value pair item for a repr."""
        return f'{self.format_obj(key, indent=indent)}: {self.format_obj(value, indent=indent)}'

    def _format_repr_id(self, obj: typing.Any) -> str:
        """Format a name for an object."""
        id_ = id(obj)
        if id_ in self._repr_id_dict:
            return self._repr_id_dict[id_]
        module = type(obj).__module__
        name = type(obj).__name__
        hex_id = hex(id_)
        if module == "builtins":
            formatted = f"[{name}.{hex_id}]"
        else:
            formatted = f"[{module}.{name}.{hex_id}]"
        self._repr_id_dict[id_] = formatted
        return formatted

    def _is_known_object(self, obj: typing.Any) -> bool:
        """Return whether obj is known."""
        return id(obj) in self._repr_id_dict

    def _format_repeated_object(self, obj: typing.Any, *, indent: str) -> str:
        """Format known object."""
        return self._format_repr_id(obj)

    def _format_dict_object(self, obj: typing.Any, *, indent: str) -> str:
        """Format dict object."""
        repr_id = self._format_repr_id(obj)

        formatted_pairs = '\n'.join(
            self._format_pair(k, value=v, indent=indent) for k, v in obj.items()
        )
        return f'{repr_id}\n{_indent(formatted_pairs, indent=indent)}'

    def _format_str_object(self, obj: typing.Any, *, indent: str) -> str:
        """Format str object."""
        repr_id = self._format_repr_id(obj)

        lines = obj.splitlines()
        indented = '\n'.join(_indent(repr(l), indent=indent) for l in lines)
        return f'{repr_id}\n{indented}'

    def _format_normal_iterable(self, obj: typing.Any, *, indent: str) -> str:
        """Format str object."""
        repr_id = self._format_repr_id(obj)
        # handle other non-generator, non-string iterable objects...
        try:
            formatted_items = '\n'.join(self.format_obj(i, indent=indent) for i in obj)
        except Exception:  # pylint: disable=broad-except
            # iterating over the object blew up - must be an unhandled special iterator
            # case.  Just return the id.
            return repr_id
        return f'{repr_id}\n{_indent(formatted_items, indent=indent)}'

    def _format_custom_repr_obj(self, obj: typing.Any, *, indent: str) -> str:
        """Format non-mixin custom repr object."""
        repr_id = self._format_repr_id(obj)
        default_repr = repr(obj)
        return f'{repr_id}\n{_indent(default_repr, indent=indent)}'

    def _format_default_repr_obj(self, obj: typing.Any, *, indent: str) -> str:
        """Format non-mixin default repr object."""
        repr_id = self._format_repr_id(obj)
        attributes = _get_repr_attributes(obj)

        # Lines
        all_lines = (repr_id,)  # type: typing.Tuple[str, ...]
        for name, value in attributes.items():
            these_lines = self._format_attribute(name, value=value, indent=indent).splitlines()
            new_lines = tuple(f"{indent}{l}" for l in these_lines)
            all_lines += new_lines
        return '\n'.join(all_lines)

    def _format_repr_mixin_obj(self, obj: typing.Any, *, indent: str) -> str:
        """Format repr_mixin object."""
        repr_id = self._format_repr_id(obj)
        # accessing private member of object this function was built
        # to work with.  Not the greatest, perhaps, but atm I don't
        # see a cleaner solution.
        # pylint: disable=protected-access
        repr_attributes = obj._repr_attributes  # noqa
        # pylint: enable=protected-access
        # set the defaults if none specified.
        if repr_attributes is None:
            attribute_names = dir(obj)
            public_attributes = (a for a in attribute_names if not a.startswith('_'))
            non_self_bound = (a for a in public_attributes if getattr(getattr(obj, a), '__self__', None) != obj)
            non_self_bound = (a for a in non_self_bound if not getattr(getattr(obj, a), '__qualname__', "").endswith(f"{obj.__class__.__name__}.{a}"))
            repr_attributes = non_self_bound
        # Data to represent
        attributes = {k: getattr(obj, k) for k in repr_attributes}
        # Lines
        all_lines = (repr_id,)  # type: typing.Tuple[str, ...]
        for name, value in attributes.items():
            these_lines = self._format_attribute(name, value=value, indent=indent).splitlines()
            new_lines = tuple(f"{indent}{l}" for l in these_lines)
            all_lines += new_lines
        return '\n'.join(all_lines)

    def format_obj(self, obj: typing.Any, *, indent: str) -> str:
        """Format an object for a nice repr."""
        # define specific formatting cases
        cases = (
            _FormatCase(self._is_known_object, self._format_repeated_object),
            _FormatCase(_is_dict, self._format_dict_object),
            _FormatCase(_is_str, self._format_str_object),
            _FormatCase(_is_normal_iterable, self._format_normal_iterable),
            _FormatCase(_is_custom_repr_obj, self._format_custom_repr_obj),
            _FormatCase(_is_repr_mixin_obj, self._format_repr_mixin_obj),
        )
        # format according to those cases
        for this_case in cases:
            if this_case.matches(obj):
                return this_case.format_(obj, indent=indent)
        # format other objects
        return self._format_default_repr_obj(obj, indent=indent)


# [ API ]
class EqualityMixin:  # not-unused: this is an API class
    """
    Provide common equality functionality.

    Behavior:
    * checks other object is an instance of this object's type
    * checks other object's attributes are the same as this object's
    * defaults to checking all attributes in __dict__
    * attributes used can be customized by setting self._equality_attributes
      `self._equality_attributes = ['one_attr', 'another_attr']`
    """

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)  # type: ignore  # https://github.com/python/mypy/issues/4335
        self._equality_attributes: typing.Optional[typing.Tuple[str, ...]] = None

    def __eq__(self, other: typing.Any) -> bool:
        # if the other isn't the same type or a subtype, return the special
        #   NotImplemented object to tell python to try the equality from the
        #   other object's perspective.
        if not isinstance(other, type(self)):
            return NotImplemented
        # Compare the equality attributes if defined.  Default to the
        #   attributes in the dict.
        equality_attributes = self._equality_attributes
        if equality_attributes is None:
            equality_attributes = tuple(k for k in self.__dict__ if k != '_equality_attributes')
        # get our data
        self_data = {k: getattr(self, k) for k in equality_attributes}
        # get the other's data.
        # we only care about the data this class cares about.  LSP says we should be
        #   able to put a Subthing() anywhere we'd put a Thing(), and that includes
        #   equality checks.  This means we can't mark not-equal due to the presence
        #   of new attributes in a subclass.
        # https://en.wikipedia.org/wiki/Liskov_substitution_principle
        other_data = {k: getattr(other, k) for k in equality_attributes}
        # actually check
        return bool(self_data == other_data)


class ReprMixin:  # not-unused: this is an API class
    r"""
    Mixin for readable, unambiguous reprs by default.

    As it's actually impossible to have eval-able reprs w/o denoting
    the full module & package version for every object in the repr, and
    that's a complex thing to provide, and nobody does that, so...
    this module instead is just really clear about module.type and
    relevant attributes.

    Since __str__ is by default __repr__, this module makes some attempts
    at decent formatting, too.

    Behaviors:
    * objects with this mixin are represented as
      f'[{module}.{type}.{hex(id(obj))}]'
      f'  name1: {repr(value1)}'
      f'  name2: {repr(value2)}'
      ...
    * indentation characters are set in the `_repr_indent` attribute
    * attributes used can be customized by setting self._repr_attributes
      `self._repr_attributes = ['one_attr', 'another_attr']`
    * objects with custom reprs are represented as
      f'[{module}.{type}.{hex(id(obj))}]\n{_indent(repr(obj), indent=indent)}'
      where the `_indent` function indents each line of the repr to the correct amount.
    * objects with default reprs are represented as if they used the mixin, and their
      _repr_attributes were set to all non-callable public attributes
    * non-generator iterables are expanded like
      f'[{module}.{type}.{hex(id(obj))}] (
      f'  {repr(item1)},
      f'  {repr(item2)},
      ...
      f')'
    * key/value items have their keys treated as values, too, and are
      represented as f'{repr(key)}: {repr(value)}'
    * multiline reprs have all lines indented to the same level as the first line.
    * recursion and other internal references are handled by only printing the
      f'[{module}.{type}.{hex(id(obj))}]' signature for objects previously encountered
      in the current repr generation.
    """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)  # type: ignore  # https://github.com/python/mypy/issues/4335
        self._repr_attributes: typing.Optional[typing.Tuple[str, ...]] = None
        self._repr_indent = 2 * ' '

    def __repr__(self) -> str:
        # the repr ID dict is meant to track per repr call.
        return _ReprFormatter().format_obj(self, indent=self._repr_indent)


FrozenMixinTypeVar = typing.TypeVar('FrozenMixinTypeVar', bound='FrozenMixin')


class FrozenMixin:  # not-unused: this is an API class
    """
    A mixin to freeze an object.

    Only freezes the object's attributes themselves, not any
    mutability within those attributes.  For instance, you can't
    say foo.my_string = 'new thing', but you can do foo.my_list.append('new thing').
    """

    @contextlib.contextmanager
    def _thawed(self) -> typing.Iterator[None]:
        stack = inspect.stack()
        caller = stack[2].frame.f_locals.get('self', None)
        func = stack[2].function
        if not (caller is self and func == '__init__'):
            raise RuntimeError("Can only thaw from __init__!")
        object.__setattr__(self, '__is_thawed', True)
        try:
            yield None
        finally:
            object.__setattr__(self, '__is_thawed', False)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        if getattr(self, '__is_thawed', False):
            object.__setattr__(self, name, value)
            return
        raise AttributeError(f"Can't set {name}, because {type(self).__name__} is frozen.")

    def copy_with(self: FrozenMixinTypeVar, **kwargs: typing.Any) -> FrozenMixinTypeVar:
        """Copy the object, but with the kwarg substitutions."""
        new_self = copy.copy(self)
        for name, value in kwargs.items():
            object.__setattr__(new_self, name, value)
        return new_self
