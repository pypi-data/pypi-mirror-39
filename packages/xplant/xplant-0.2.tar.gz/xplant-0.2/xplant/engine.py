import weakref


class NodeBase(object):
    __slots__ = ("children", "__plant")

    def __init__(self, plant_instance):
        self.children = []
        self.__plant = weakref.ref(plant_instance) if plant_instance else None

    @property
    def plant(self):
        return self.__plant() if self.__plant else None

    def __enter__(self):
        plant = self.plant
        if plant:
            plant.enter_(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        plant = self.plant
        if plant:
            plant.exit_()

    def __str__(self):
        return "".join(item for item in self.string_items(0) if item)

    def string_items(self, tree_level):
        msg = "\n".join([
            "NodeBase.string_items is an abstract method.", "",
            "It's supposed to:",
            " - be a generator yielding string items,",
            " - compose document representation of that node with ''.join(node.string_items(0)),",
            " - care for document's line breaks, markup and indentation.",
            "It needs to be implemented in derived class {name!r}.",
            ""
        ])
        raise NotImplementedError(msg.format(name=self.__class__.__name__))

    def append_child_node(self, new_node_obj):
        if not isinstance(new_node_obj, NodeBase):
            raise TypeError("Can append only instances of NodeBase, got {}.".format(type(new_node_obj).__name__))
        self.children.append(new_node_obj)

    @property
    def degree(self):
        """ For a given node, its number of children. A leaf is necessarily degree zero. """
        return len(self.children)

    @property
    def height(self):
        """ The height of a node is the number of edges on the longest path between that node and a leaf. """
        if not self.children:
            return 0
        else:
            return 1 + max(child.height for child in self.children)

    def _make_child(self, node_class, *args, **kwargs):
        if not issubclass(node_class, NodeBase):
            raise TypeError("Node class has to be a subclass of NodeBase, got %s." % node_class.__name__)
        new_node_instance = node_class(self.plant, *args, **kwargs)
        self.append_child_node(new_node_instance)
        return new_node_instance

    @classmethod
    def make_root(cls, plant_instance):
        """ Modify own class to be able to create a document plant - i.e. forest - collection of disjoint trees.
            IT can appear only on document's zero level, """

        class RootNode(cls):
            def __init__(self):
                NodeBase.__init__(self, plant_instance)

            def string_items(self, _):
                for child in self.children:
                    for item in child.string_items(tree_level=0):
                        yield item

        RootNode.__name__ = "{}Root".format(cls.__name__)
        return RootNode()


class LeafNodeMixin(object):
    """ Leaf - a node that is not allowed to have children. """

    def append_child_node(self, new_node_obj):
        raise AttributeError("{} is not allowed to append any children".format(self.__class__.__name__))

    def __enter__(self):
        msg = "Instance of {} cannot enter its scope, it's a leaf. Call it as a regular method (w/o 'with')."
        raise AttributeError(msg.format(self.__class__.__name__))


class XPlant(object):
    _root_node_type = None

    def __init__(self):
        assert self._root_node_type, "Undefined primary node for {}".format(self.__class__.__name__)
        assert issubclass(self._root_node_type, NodeBase), "Wrong primary node type {}".format(
            self._root_node_type)

        self.__tag_stack = [self._root_node_type.make_root(self)]

    def __str__(self):
        return str(self.__tag_stack[0])

    def __repr__(self):
        return "{}(<{}>)".format(type(self).__name__, type(self.__tag_stack[0]).__name__)

    @property
    def _top_node(self):
        """ The node whose context we are currently in. """
        return self.__tag_stack[-1]

    def __getattr__(self, attribute_name):
        """ Expose interface of a node that is currently on top (whose context we are currently in). """
        is_not_protected = not attribute_name.startswith("_")
        if is_not_protected and hasattr(self._top_node, attribute_name):
            return object.__getattribute__(self._top_node, attribute_name)

        return object.__getattribute__(self, attribute_name)

    def enter_(self, obj):
        self.__tag_stack.append(obj)

    def exit_(self):
        self.__tag_stack.pop()
