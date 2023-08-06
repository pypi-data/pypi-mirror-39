from datahelper.private.is_numeric import is_numeric


def cast_path(path_like):
    if is_numeric(path_like):
        return int(path_like)
    return str(path_like)
