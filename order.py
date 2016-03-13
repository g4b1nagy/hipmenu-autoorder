import importlib


config = importlib.import_module('config')
config = {key: getattr(config, key) for key in dir(config) if key.isupper()}


if __name__ == '__main__':
    print('end')
