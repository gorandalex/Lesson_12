#import random
from adressbook import *
import os

if os.path.exists(os.path.join(os.path.dirname('.'), 'AdressBook.dat')):
    dict_telephones = AdressBook.read_from_file('AdressBook.dat')
else:
    dict_telephones = AdressBook()

def input_error(func):
    """Обробляемо помилки, якіх міг припуститись користувач"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Ви ввели не вірне ім'я"
        except TypeError:
            return "Ви ввели не вірний форат команди"
        except IndexError:
            return "Введіть ім'я та телефон"
        except ValueError as e:
            return e.args[0]
        except Exception as e:
            return e.args

    return wrapper


@input_error
def answer_hello():
    """Привітаємо користувача"""
    return 'How can I help you?'

@input_error
def answer_add(data_record):
    """Додаємо телефон до словника"""
    lst_data_record = data_record.strip().split()
    name = lst_data_record[0]
    telephone = lst_data_record[1]
    birthday = ''
    if len(lst_data_record) > 2:
        birthday = lst_data_record[2]

    if name in dict_telephones:
        record = dict_telephones.data[name]
        record.add_phone(telephone)
    else:
        record = Record(name, telephone, birthday)
        dict_telephones.add_record(record)

    return f'Для {name} записан телефон {telephone}'

@input_error
def answer_change(name_telephone):
    """Змінюємо телефон в словнику"""
    lst_name_telephone = name_telephone.strip().split()
    name = lst_name_telephone[0]
    old_telephone = lst_name_telephone[1]
    telephone = lst_name_telephone[2]
    record = dict_telephones.data[name]
    record.change_phone(old_telephone, telephone)
    return f'Для {name} змінено телефон {old_telephone} на {telephone}'

@input_error
def answer_phone(name):
    """Повертаємо телефон за ім'ям"""
    record = dict_telephones.data[name]
    return ', '.join([phone.value for phone in record.phones])


@input_error
def answer_showall():
    """Виводимо всі телефони"""
    text_phones = ''
    for name, record in dict_telephones.items():
        text_phones += name + ' ' + ', '.join([phone.value for phone in record.phones]) + '\n'
    return text_phones

@input_error
def answer_find(text):
    answer_records = ''
    for record in dict_telephones.find_records_by_text(text):
        answer_records += record + '\n'
    return answer_records

@input_error
def answer_exit():
    return 'Good bye!'

@input_error
def command_error():
    return 'Ви ввели не вірну команду'

"""Створимо словник команд для пошуку потрібних методів"""
DICT_COMMANDS = {
                    'hello': answer_hello,
                    'add': answer_add,
                    'change': answer_change,
                    'phone': answer_phone,
                    'show all': answer_showall,
                    'find': answer_find,
                    'exit': answer_exit,
                    'good bye': answer_exit,
                    'close': answer_exit
                }

def get_answer_function(answer):
    """Повертаємо потрибний метод для команди користувача"""
    return DICT_COMMANDS.get(answer, command_error)


@input_error
def run_command(user_command):
    command = user_command
    params = ''
    for key in DICT_COMMANDS:
        if user_command.lower().startswith(key):
            command = key
            params = user_command[len(command):]
            break
    if params:
        return get_answer_function(command)(params.strip())
    else:
        return get_answer_function(command)()


def main():

#    for _ in range(100):
#        a = random.randint(1, 100)
#        i = random.randint(1000000, 9999999)
#        answer_add(
#            f'{a} +38063{i} {random.randint(1, 28)}.{random.randint(1, 12)}.{random.randint(1980, 2000)}')


    while True:
        user_command = input('Введіть команду для бота: ')
        answer = run_command(user_command.strip())
        print(answer)
        if answer == 'Good bye!':
            break
    dict_telephones.save_to_file('AdressBook.dat')
    
#    for record in dict_telephones.iterator(5):
#        print(record)
#        print('========================================================')

if __name__ == "__main__":
    main()