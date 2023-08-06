from os.path import join, abspath
from abc import abstractmethod
import json


class Base:
    def __init__(self, path_to_dump, verbose=0):
        self._path = abspath(path_to_dump)
        self._verbose = verbose
        self._startup()
        pass

    @staticmethod
    def __parse_obj(obj):
        for key in obj:
            if type(obj[key]) is str:
                obj[key] = obj[key].encode('latin_1').decode('utf-8')
                pass
            elif type(obj[key]) is list:
                obj[key] = list(map(lambda x: x if type(x) != str else x.encode('latin_1').decode('utf-8'), obj[key]))
            pass
        return obj

    def _register_files(self, files: dict):
        for name in files:
            file = files[name]
            path = join(self._path, file)

            with open(path) as f:
                setattr(self, name, json.load(f, object_hook=self.__parse_obj))
                pass
            pass
        pass

    def parse_file(self, file, join_with_dump_path=True):
        with open(join(self._path, file) if join_with_dump_path else file) as f:
            data = json.load(f, object_hook=self.__parse_obj)
            pass
        return data

    def _get_file(self, file):
        with open(join(self._path, file)) as f:
            return json.load(f, object_hook=self.__parse_obj)
        pass

    @abstractmethod
    def _startup(self):
        pass
    pass
