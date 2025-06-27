# sitecustomize.py

# Monkey-patch Pydantic’s deprecated root_validator to always include skip_on_failure=True,
# so that libraries using Pydantic v1-style @root_validator work under Pydantic v2.
import pydantic

try:  # Only available in Pydantic v2
    import pydantic.deprecated.class_validators as _cv  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - running under Pydantic v1
    _cv = None

if _cv is not None:
    _original_root_validator = _cv.root_validator

    def root_validator(pre: bool = False, skip_on_failure: bool = True, allow_reuse: bool = False):
        """Wrap original root_validator forcing skip_on_failure=True."""
        return _original_root_validator(pre=pre, skip_on_failure=skip_on_failure, allow_reuse=allow_reuse)

    # Override the root_validator in the Pydantic deprecated module
    _cv.root_validator = root_validator


# Monkey-patch Pydantic’s conlist only when running under Pydantic v2.
if pydantic.version.VERSION.startswith("2"):
    import pydantic.types as _types

    _original_conlist = pydantic.conlist

    def conlist(item_type, *args, min_items=None, max_items=None, **kwargs):
        """Map min_items/max_items to min_length/max_length."""
        return _original_conlist(
            item_type,
            *args,
            min_length=min_items,
            max_length=max_items,
            **kwargs,
        )

    # Override both references to conlist
    pydantic.conlist = conlist
    _types.conlist = conlist
