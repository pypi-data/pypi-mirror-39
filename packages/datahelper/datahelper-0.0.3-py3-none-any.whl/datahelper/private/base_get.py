from datahelper.private.cast_path import cast_path


def base_get(obj, path):
    key = cast_path(path)

    try:
        return obj.__getitem__(key)
    except (KeyError, IndexError, AttributeError, TypeError):
        return None
