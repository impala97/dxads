import sys


class config:
    __username__ = None
    __id__ = 0
    __email__ = None

    def __call__(self, username=None,id=0,email=None):
        if username is not None:
            self.__username__ = username

        if id is not None:
            self.__id__ = id

        if email is not None:
            self.__email__ = email



if __name__ == '__main__':
    config()