import json


def get_data_from_file(filename):
    try:
        with open(filename) as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(e)


def write_to_file(filename, data):
    try:
        data_file = get_data_from_file(filename)
        if not data_file:
            lst = []
            with open(filename, 'w') as file:
                lst.append(data)
                json.dump(lst, file)
        else:
            with open(filename, 'w') as file:
                data_file.append(data)
                json.dump(data_file, file)
    except Exception as e:
        print(e)


def get_user_from_file(filename, id) -> bool | dict:
    try:
        with open(filename) as file:
            data = json.load(file)
            for user in data:
                if user.get('id') == id:
                    return user
        return False
    except Exception as e:
        print(e)
        return False