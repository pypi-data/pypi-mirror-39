from datahelper.private.is_numeric import is_numeric


def create(path):
    if is_numeric(path):
        return []
    return {}
