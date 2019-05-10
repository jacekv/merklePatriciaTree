
class DB:
    __instance = None
    db = {}

    def __init__(self):
        """
        Virtually private constructor.
        """
        if DB.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DB.__instance = self

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DB.__instance == None:
            DB()
        return DB.__instance

    def put(self, key, data):
        self.db[key] = data

    def get(self, key):
        if key in self.db:
            return self.db[key]
        return None

    def delete(self, key):
        if key in self.db:
            del self.db[key]

    def commit(self):
        return


