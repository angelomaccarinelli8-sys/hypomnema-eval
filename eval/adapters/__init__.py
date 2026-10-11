from .echo import EchoAdapter
from .hypomnema_jsonl import HypomnemaJsonlAdapter


def get_adapter(adapter_type: str):
    if adapter_type == "echo":
        return EchoAdapter()
    if adapter_type == "hypomnema_jsonl":
        return HypomnemaJsonlAdapter()
    raise ValueError(f"Unknown adapter_type: {adapter_type}")
