import re
from datetime import datetime
import decorators
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

    def iterator(self):
        pass


address_book = AddressBook()


def hello_handler():
    return 'How can I help you?'


@decorators.add_error_decorator
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


@decorators.change_error_decorator
def change_handler(*args):
    old_phone = Phone(args[1])
    phone = Phone(args[2])
    record = address_book.data[args[0]]
    if record.change_phone(old_phone, phone):
        return 'Telephone number has beem changed'


@decorators.phone_error_decorator
def phone_handler(*args):
    return address_book[args[0]]


def show_all_handler():
    return "\n".join((f"{values} " for values in address_book.values()))


def days_to_birthday_handler(*args):
    record = address_book[args[0]]
    s_record = (repr(record))
    date = re.search(r'\d{2}\.\d{2}\.\d{4}', s_record)
    birthday = Birthday(date.group())
    result = record.days_to_birthday(birthday)
    return result


def exit1_handler():
    return 'Good bye!'


def exit2_handler():
    return 'Good bye!'


def exit3_handler():
    return 'Good bye!'


commands = {
    hello_handler: 'hello',
    add_handler: 'add',
    change_handler: 'change',
    phone_handler: 'phone',
    show_all_handler: 'show all',
    days_to_birthday_handler: 'birthday',
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


@decorators.input_error_decorator
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
