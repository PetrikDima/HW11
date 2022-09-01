def add_error_decorator(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return 'If you write command "add" please write "add" "name" "number"'
        except KeyError:
            return "..."

    return wrapper


def change_error_decorator(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return 'If you write command "change" please write "change" "name" "number"'
        except KeyError:
            return "..."

    return wrapper


def phone_error_decorator(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return 'If you write command "phone" please write "phone" "name"'
        except KeyError:
            return "..."

    return wrapper


def input_error_decorator(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return 'You have written unknown command'
        except AttributeError:
            return '...'

    return wrapper

