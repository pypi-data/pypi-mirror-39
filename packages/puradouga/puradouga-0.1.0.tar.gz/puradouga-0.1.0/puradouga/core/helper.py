import copy
from typing import Optional, Dict, Any, List, ClassVar


def args_kwargs_decorator(names: Optional[Dict[str, Any]] = None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            for item in names.items():
                kwargs.setdefault(item[0], copy.deepcopy(item[1]))
            return f(*args, **kwargs)
        return wrapper
    return decorator


def order_by_list(order: List[str]):
    order = list(reversed(order))

    def _order(plugin: ClassVar):
        try:
            return order.index(plugin.__class__.__name__)
        except ValueError:
            return -1
    return _order
