class AttributeFloater(set):
    """
        It's a helper that tells us whether we would like
        to get given attribute from given instance or redirect
        getattribute call to the most top instance in current
        tree model branch.
    """

    def __init__(self, *args, **kwargs):
        super(AttributeFloater, self).__init__(*args, **kwargs)
        self.fixed = set()

    @staticmethod
    def is_public(attribute_name):
        return not attribute_name.startswith("_")

    def all_attrs_float(self, cls):
        """ Makes each attribute floating unless it has been already marked as fixed e.g. in base class. """
        for attribute_name in cls.__dict__:
            if self.is_public(attribute_name) and attribute_name not in self.fixed:
                self.add(attribute_name)
        return cls

    def all_attrs_fixed(self, cls):
        for attribute_name in cls.__dict__:
            if self.is_public(attribute_name):
                self.fixed.add(attribute_name)
        return cls
