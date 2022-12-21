import plyvel

class DB:
    __instance = None

    def __init__(self, path, create_if_missing=True):
        """
        Virtually private constructor.
        """
        if self.__instance == None:
            self.__instance = plyvel.DB(path, create_if_missing=create_if_missing)

    def put(self, key, data):
        self.__instance.put(key, data)

    def get(self, key):
        return self.__instance.get(key)

    def delete(self, key):
        self.__instance.delete(key)



