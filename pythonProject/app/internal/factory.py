from typing import Callable, Any
from fastapi import APIRouter

router_creation_funcs: dict[str, Callable[..., APIRouter]] = {}


def register(router_type: str, creation_function: Callable[..., APIRouter]):
    """Register a new APIRouter Type"""
    router_creation_funcs[router_type] = creation_function


def unregister(router_type: str):
    """Unregister APIRouterType"""
    router_creation_funcs.pop(router_type, None)


def create(arguments: dict[str, Any]):
    """Create a APIRouter"""
    args_copy = arguments.copy()
    router_type = args_copy.pop("type")
    try:
        creation_fun = router_creation_funcs[router_type]
        return creation_fun(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown router type {router_type}") from None