class Storage:
    def __init__(self, storage={}):
        self.storage = storage

    def set_storage(self, key, val):
        if key not in self.storage.keys():
            self.storage[key] = []
        self.storage[key] = val
