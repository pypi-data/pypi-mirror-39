'''
DAL = Data Access Layer
'''

class DAL: # Data Access Layer Base class

    def insert(cls, **kwargs):
        '''

        :param kwargs:
        :return:
        '''

    def update(cls, **kwargs):
        '''

        :param kwargs:
        :return:
        '''

    def delete(cls, **kwargs):
        '''

        :param kwargs:
        :return:
        '''

    def get(self, key, default='nullid'):
        '''

        :param key:
        :return:
        '''

class Simpledal(DAL):

    __instance = None
    def __new__(cls):
        if Simpledal.__instance is None:
            Simpledal.__instance = object.__new__(cls)

        return Simpledal.__instance


    def insert(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)


    def update(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)


    def delete(self, key):
        delattr(self, key)


    def get(self, key, default='nullid'):
        return getattr(self, key, default)

