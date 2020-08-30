def pick_keys(d, keys):
    """Return dictionary d with only the specified keys."""
    return {k: v for k, v in d.items() if k in keys}
