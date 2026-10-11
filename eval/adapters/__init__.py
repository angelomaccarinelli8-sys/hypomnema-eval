from .echo import EchoAdapter


def get_adapter(adapter_type: str):
    if adapter_type == "echo":
        return EchoAdapter()
    raise ValueError(f"Unknown adapter_type: {adapter_type}")
