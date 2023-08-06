def represent_int(int_like):
    try:
        int(int_like)
        return True
    except ValueError:
        return False