from datahelper.private.cast_path import cast_path
from datahelper.private.is_numeric import is_numeric


def base_set(obj, path, value):
    new_object = obj.copy()
    try:
        if is_numeric(path):
            try:
                index = cast_path(path)
                new_object.insert(index, value)
                return new_object
            except AttributeError:
                return [value]
        new_object[path] = value
        return new_object
    except IndexError:
        new_object.append(value)
        return new_object
    except TypeError:
        return {
            path: value
        }


def main():
    dummy = [1, 2, 3, 4]
    result = base_set(dummy, '4', 10)
    print(result)


if __name__ == '__main__':
    main()
