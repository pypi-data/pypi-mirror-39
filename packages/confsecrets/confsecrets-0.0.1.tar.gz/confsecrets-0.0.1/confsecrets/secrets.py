"""
Implement secrets that know their type and are stored in a vault
"""
from .vault import DefaultVault

__all__ = (
    'BaseSecret',
    'Secret',
)


class BaseSecret:
    """
    A secret is stored in a vault using a string name
    """

    def __init__(self, name, vault=None):
        self.name = str(name)
        if vault is None:
            vault = DefaultVault()
        self.vault = vault

    def get(self):
        return self.vault[self.name]

    def set(self, value):
        self.vault[self.name] = value

    def decrypt(self):
        return self.get()

    def __repr__(self):
        return '<%s name=%s>' % (type(self), self.name)


class Secret(BaseSecret):
    """
    Usually secrets are strings
    """
    def __str__(self):
        return self.get()

    def __contains__(self, item):
        return item in self.__str__()

    def __iter__(self):
        for c in self.__str__():
            yield c

    def __bool__(self):
        return self.get().lower() in ('yes', 'true', '1')

    def __int__(self):
        return int(self.get())

    def strip(self, *args):
        return self.__str__().strip(*args)

    def startswith(self, *args):
        return self.__str__().startswith(*args)

    def endswith(self, *args):
        return self.__str__().endswith(*args)

    def replace(self, *args):
        return self.__str__().replace(*args)
