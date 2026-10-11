def normalize(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def exact_match(pred: str, ref: str) -> float:
    return 1.0 if normalize(pred) == normalize(ref) else 0.0


def f1_token(pred: str, ref: str) -> float:
    p_tokens = normalize(pred).split()
    r_tokens = normalize(ref).split()

    if not p_tokens and not r_tokens:
        return 1.0
    if not p_tokens or not r_tokens:
        return 0.0

    common = {}
    for t in p_tokens:
        common[t] = common.get(t, 0) + 1

    overlap = 0
    for t in r_tokens:
        if common.get(t, 0) > 0:
            overlap += 1
            common[t] -= 1

    if overlap == 0:
        return 0.0

    precision = overlap / len(p_tokens)
    recall = overlap / len(r_tokens)
    return 2 * precision * recall / (precision + recall)


def faithfulness_heuristic(pred: str, context: str) -> float:
    """
    Placeholder metric: checks whether prediction string appears in context.
    Replace with stronger attribution/claim-grounding evaluator.
    """
    p = normalize(pred)
    c = normalize(context)
    if not p:
        return 0.0
    return 1.0 if p in c else 0.0
