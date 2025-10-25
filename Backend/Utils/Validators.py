def strip_string(v, skip_fields=None, field_name=None):
    """Strips whitespace from strings, skipping specified fields (like passwords)."""
    if isinstance(v, str):
        if skip_fields and field_name in skip_fields:
            return v
        return v.strip()
    return v


def capitalize_field(v):
    """Capitalizes names, places, and similar text fields."""
    if isinstance(v, str):
        return v.strip().capitalize()
    return v


def clean_id_number(v):
    """Removes spaces in ID numbers."""
    if isinstance(v, str):
        return v.replace(" ", "")
    return v


def normalize_email(v):
    """Strips and lowercases emails."""
    if isinstance(v, str):
        return v.strip().lower()
    return v
