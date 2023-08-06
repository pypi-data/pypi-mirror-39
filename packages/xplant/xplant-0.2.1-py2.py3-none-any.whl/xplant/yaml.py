from .engine import XPlant, NodeBase


def NodeDescriptor(*a):
    pass


class PYamlNode(NodeBase):
    _single_indent = '  '
    __slots__ = "value",

    def __init__(self, plant_instance, value):
        super(PYamlNode, self).__init__(plant_instance)
        self.value = value

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.value)

    def string_items(self, tree_level):
        representation = "{} - {}".format(self._single_indent * tree_level, self.value)
        if self.children:
            representation += ":"
        yield representation + "\n"

        for child in self.children:
            for item in child.string_items(tree_level + 1):
                yield item

    def node(self, value):
        return self._make_child(PYamlNode, value)

    def leaf(self, value):
        return self._make_child(PYamlNode, value)


class PYamlPlant(XPlant):
    _root_node_type = PYamlNode
