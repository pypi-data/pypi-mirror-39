from scopeton import scopeTools
from scopeton.scopeTools import getBean_qualifier


class Bean(object):
    def __init__(self, cls, name=None, lazy = False, singleton=True, service = True, checkRegistered = True):
        self.checkRegistered = True
        self.cls = cls
        self.qualifier_tree = scopeTools.getClassTreeQualifiers(cls)
        if name:
            name = getBean_qualifier(name)
            if name not in self.qualifier_tree:
                self.qualifier_tree.append(name)
        self.lazy = lazy
        self.singleton = singleton
        self.service = service
        if not singleton and service:
            raise Exception("Error, cannot initialize service as non singleton")

    def __hash__(self):
        return hash(self.cls)

    def __eq__(self, other):
        return self.cls == other.cls


    def __repr__(self):
        return str(self)
    def __str__(self):
        name = self.__class__.__name__ if hasattr(self.__class__, "__name__") else str(self.__class__)
        return "{name}[{qualifier}]".format(self=self, name=name, qualifier=self.qualifier_tree[-1])

