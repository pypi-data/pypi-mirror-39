from xplant.engine import LeafNodeMixin
from .engine import XPlant, NodeBase
from ._xml_attributes import XmlAttributes


class _XmlMarkupBase(NodeBase):
    __slots__ = "_value",
    _format = "{}"

    def __init__(self, plant_instance, value):
        super(_XmlMarkupBase, self).__init__(plant_instance)
        self._value = value

    def string_items(self, tree_level):
        yield self._format.format(self._value)


class Text(LeafNodeMixin, _XmlMarkupBase):
    pass


class Comment(LeafNodeMixin, _XmlMarkupBase):
    _format = "<!-- {} -->"


class CdataTag(LeafNodeMixin, _XmlMarkupBase):
    _format = "<![CDATA[{}]]>"


class _XmlElementNodeBase(NodeBase):
    attribute_processor = XmlAttributes
    _force_inline = False
    __slots__ = ("tag_name", "attributes",)
    indent_value = 2 * " "

    def __init__(self, plant_instance, tag_name, *args, **kwargs):
        super(_XmlElementNodeBase, self).__init__(plant_instance)
        self.tag_name = tag_name
        self.attributes = self.attribute_processor(*args, **kwargs)

    @classmethod
    def _break_line(cls, tree_level):
        indent = cls.indent_value
        return "\n" + indent * tree_level


class EmptyXmlElement(LeafNodeMixin, _XmlElementNodeBase):
    """ E.g.: <br />, <hr /> or <img src="#" alt="" /> """

    def string_items(self, tree_level):
        yield "<{}{} />".format(self.tag_name, self.attributes)


class XmlElement(_XmlElementNodeBase):

    def node(self, name, *p, **k):
        p = (name,) + p
        return self._make_child(XmlElement, *p, **k)

    def leaf(self, name, *p, **k):
        p = (name,) + p
        return self._make_child(EmptyXmlElement, *p, **k)

    def text(self, string_value):
        return self._make_child(Text, string_value)

    def cdata(self, string_value):
        return self._make_child(CdataTag, string_value)

    def comment(self, string_value):
        return self._make_child(Comment, string_value)

    def line(self, tag_name, content, *args, **kwargs):
        """ Element containing just a text. """
        with self.node(tag_name, *args, **kwargs):
            self.text(content)

    def string_items(self, tree_level):
        yield "<{}{}>".format(self.tag_name, self.attributes)
        for item in self._children_markup(tree_level):
            yield item
        yield "</{}>".format(self.tag_name)

    def _children_markup(self, tree_level):
        break_lines = self.degree > 1 and not self._force_inline
        child_indent = self._break_line(tree_level + 1)

        for child in self.children:
            if break_lines:
                yield child_indent

            for child_string in child.string_items(tree_level + 1):
                yield child_string

        if break_lines:
            yield self._break_line(tree_level)


class XmlPlant(XPlant):
    _root_node_type = XmlElement
