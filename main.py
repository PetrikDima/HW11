from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value: str):
        self._value = None

        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    @Field.value.setter
    def value(self, value):
        if isinstance(value, str):
            self._value = value
        else:
            raise ValueError('Name must be string')

    def __repr__(self):
        return self._value


class Phone(Field):
    @Field.value.setter
    def value(self, value: str):
        if len(value) == 13 and value.startswith('+38') or len(value) == 10 and value.startswith('0'):
            self._value = value
        else:
            raise ValueError("Phone number isn't correct")

    def __repr__(self):
        return self._value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            print('Wrong format of Birthday')

    def __repr__(self):
        return datetime.strftime(self._value, "%d.%m.%Y")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name: Name = name
        self.phone: list[Phone] = [phone] if phone is not None else []
        self.birthday = birthday

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            self.phone.remove(old_phone)
            self.phone.append(new_phone)
        except ValueError:
            return f'Old_phone: {old_phone} has not existed to change'

    def remove_phone(self, phone: Phone):
        try:
            self.phone.remove(phone)
        except ValueError:
            return f'Phone: {phone} has not existed to delete'

    def days_to_birthday(self):
        time_now = datetime.now()
        pattern = self.birthday.value.replace(year=time_now.year)
        diff = pattern - time_now.date()
        if -365 <= diff.days <= -1:
            diff1 = 365 + diff.days
            return f"{diff1} days to birthday"
        else:
            return f"{diff.days} days to birthday"

    def __repr__(self):
        if self.birthday is not None:
            return f'{self.name} {self.phone} {self.birthday}'
        return f'{self.name} {self.phone}'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, max_count):
        count = 0
        for item in self.data:
            if count < max_count:
                count += 1
                yield self.data[item]
        else:
            raise StopIteration


address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return """If you write command 'add' please write 'add' 'name' 'number'
If you write command 'change' please write 'change' 'name' 'number'
If you write command 'phone' please write 'phone' 'name'
If you write command 'remove' please write 'remove' 'name' 'number'
If you write command 'records' please write 'records' and number of records"""
        except KeyError:
            return "This key not found try again"
        except TypeError:
            return "Type not supported try again"
        except ValueError:
            return "Incorrect value try again"
        except AttributeError:
            return "Incorrect attribute try again"
        except StopIteration:
            return "That's all"
        except RuntimeError:
            return "..."

    return wrapper


@input_error
def hello_handler():
    return 'How can I help you?'


@input_error
def add_handler(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    try:
        birthday = Birthday(args[2])
    except IndexError:
        birthday = None
        print('Date has not exist')
    record = Record(name, phone, birthday)
    address_book.add_record(record)
    return 'Telephone number has beem added'


@input_error
def change_handler(*args):
    old_phone = Phone(args[1])
    phone = Phone(args[2])
    record = address_book.data[args[0]]
    if record.change_phone(old_phone, phone):
        return 'Telephone number has beem changed'


@input_error
def phone_handler(*args):
    return address_book[args[0]]


@input_error
def show_all_handler():
    return "\n".join([f"{v} " for v in address_book.values()])


@input_error
def show_n_handler(*args):
    for item in address_book.iterator(int(args[0])):
        print(item)


@input_error
def days_to_birthday_handler(*args):
    record = address_book[args[0]]
    result = record.days_to_birthday()
    return result


@input_error
def exit1_handler():
    return 'Good bye!'


@input_error
def exit2_handler():
    return 'Good bye!'


@input_error
def exit3_handler():
    return 'Good bye!'


commands = {
    hello_handler: 'hello',
    add_handler: 'add',
    change_handler: 'change',
    phone_handler: 'phone',
    show_all_handler: 'show all',
    days_to_birthday_handler: 'birthday',
    show_n_handler: 'records',
    exit1_handler: 'exit',
    exit2_handler: 'close',
    exit3_handler: 'good bye',
}


def user_input_parser(user_input):
    data = []
    command = ""
    for k, v in commands.items():
        if user_input.startswith(v):
            command = k
            data = user_input.replace(v, "").split()
        if user_input == "":
            main()
    return command, data


@input_error
def main():
    while True:
        user_input = input('Command: ').lower()
        command, arguments = user_input_parser(user_input)
        print(command(*arguments))
        if command == exit1_handler or command == exit2_handler or command == exit3_handler:
            break


if __name__ == '__main__':
    main()
# add dima +380975323736 25.05.2004
# add bob +380653432716 27.12.2003
# add max +380725679728 1.11.2002
# add ann +380984322716 12.6.2006
