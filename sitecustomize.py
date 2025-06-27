# sitecustomize.py

# Monkey-patch Pydantic’s deprecated root_validator to always include skip_on_failure=True,
# so that libraries using Pydantic v1-style @root_validator work under Pydantic v2.
import pydantic.deprecated.class_validators as _cv

_original_root_validator = _cv.root_validator

def root_validator(pre: bool = False, skip_on_failure: bool = True, allow_reuse: bool = False):
    """
    Wrap the original root_validator and force skip_on_failure=True by default.
    This ensures Pydantic v1 style validators don’t break under Pydantic v2.
    """
    return _original_root_validator(pre=pre, skip_on_failure=skip_on_failure, allow_reuse=allow_reuse)

# Override the root_validator in the Pydantic deprecated module
_cv.root_validator = root_validator


# Monkey-patch Pydantic’s conlist to map old min_items/max_items args
# to the new min_length/max_length expected by Pydantic v2.
import pydantic
import pydantic.types as _types

_original_conlist = pydantic.conlist

def conlist(item_type, *args, min_items=None, max_items=None, **kwargs):
    """
    Wrap the original conlist and translate:
      - min_items → min_length
      - max_items → max_length
    This allows libraries using conlist(min_items=…) to continue working.
    """
    return _original_conlist(
        item_type,
        *args,
        min_length=min_items,
        max_length=max_items,
        **kwargs
    )

# Override both references to conlist
pydantic.conlist = conlist
_types.conlist = conlist
