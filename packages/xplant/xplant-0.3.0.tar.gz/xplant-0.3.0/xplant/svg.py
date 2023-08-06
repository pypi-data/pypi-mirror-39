from .engine import LeafNodeMixin
from .xml import XmlAttributes, XmlElement


class SvgAttributes(XmlAttributes):
    attribute_name_substitutes = {
        'klass': 'class',
        'Class': 'class',
        'class_': 'class',
        'fill_opacity': 'fill-opacity',
        'stroke_width': 'stroke-width',
        'stroke_dasharray': ' stroke-dasharray',
        "stroke_opacity": "stroke-opacity",
        "stroke_dashoffset": "stroke-dashoffset",
        "stroke_linejoin": "stroke-linejoin",
        "stroke_linecap": "stroke-linecap",
        "stroke_miterlimit": "stroke-miterlimit",
    }


class SvgNode(XmlElement):
    _attribute_processor = SvgAttributes

    def __init__(self, parent_node_, tag_name, *xml_args, **xml_kwargs):
        super(SvgNode, self).__init__(parent_node_, tag_name, *xml_args, **xml_kwargs)

    @staticmethod
    def _replicant_leaf_type():
        return SvgLeaf

    @classmethod
    def _root_head_items(cls):
        yield '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'
        yield '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'


class SvgLeaf(LeafNodeMixin, SvgNode):
    def string_items(self, tree_level):
        yield "<{}{} />".format(self.tag_name, self.attributes)


def svg_plant():
    return SvgNode(None, None)
