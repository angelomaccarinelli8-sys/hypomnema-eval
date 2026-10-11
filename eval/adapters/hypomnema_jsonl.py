import json
from pathlib import Path

from .base import BaseAdapter


def _normalize(text: str) -> list[str]:
    return [t for t in " ".join((text or "").lower().split()).split(" ") if t]


class HypomnemaJsonlAdapter(BaseAdapter):
    """
    Minimal local adapter for memory retrieval from a JSONL store.

    Behavior:
    - If memory_enabled is false: return empty string (baseline behavior).
    - If memory_enabled is true: load JSONL entries and return best lexical-overlap match.

    JSONL entry supports:
    - text (preferred)
    - content (fallback)
    """

    def _load_entries(self, memory_store_path: str) -> list[str]:
        path = Path(memory_store_path)
        if not path.exists():
            return []

        entries = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                text = (obj.get("text") or obj.get("content") or "").strip()
                if text:
                    entries.append(text)
        return entries

    def _best_match(self, query: str, entries: list[str]) -> str:
        q_tokens = set(_normalize(query))
        if not q_tokens or not entries:
            return ""

        best_score = -1
        best_text = ""
        for text in entries:
            t_tokens = set(_normalize(text))
            score = len(q_tokens.intersection(t_tokens))
            if score > best_score:
                best_score = score
                best_text = text
        return best_text

    def answer(self, sample: dict, config: dict) -> str:
        adapter_cfg = config.get("adapter", {})
        memory_enabled = bool(adapter_cfg.get("memory_enabled", False))
        if not memory_enabled:
            return ""

        store_path = adapter_cfg.get("memory_store_path", "")
        entries = self._load_entries(store_path)
        question = sample.get("question", "")
        return self._best_match(question, entries)
