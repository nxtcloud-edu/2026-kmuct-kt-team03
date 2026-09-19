def rank_notices(notices):
    return sorted(
        notices,
        key=lambda x: x["relevance"],
        reverse=True
    )