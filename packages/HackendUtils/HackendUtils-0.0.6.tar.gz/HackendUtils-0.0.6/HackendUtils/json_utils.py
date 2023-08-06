import json


def load(path):
    try:
        with open(path) as file:
            return json.load(file)
    except IOError:
        return


def write(json_data, path):
    f1 = open(path, 'w+')
    f1.write(json_data)
    f1.close()
