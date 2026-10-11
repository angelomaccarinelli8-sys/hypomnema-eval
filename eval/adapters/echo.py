from .base import BaseAdapter


class EchoAdapter(BaseAdapter):
    """
    Minimal adapter: returns the expected answer if provided by sample payload.
    This is a stub to make the harness runnable out-of-the-box.
    Replace with real integration adapter(s).
    """

    def answer(self, sample: dict, config: dict) -> str:
        return sample.get("answer", "")
