def is_numeric(int_like):
    try:
        int(int_like)
        return True
    except ValueError:
        return False
