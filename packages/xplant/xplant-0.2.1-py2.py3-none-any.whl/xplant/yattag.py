from contextlib import contextmanager

from .xml import XmlPlant


class YattagPlant(XmlPlant):
    """ Exposes an interface similar to yattag's simpledoc. """

    @contextmanager
    def tag(self, tag_name, *args, **kwargs):
        with self.node(tag_name, *args, **kwargs):
            yield

    def stag(self, tag_name, *args, **kwargs):
        """ Empty xml element. """
        self.leaf(tag_name, *args, **kwargs)

    def tagtext(self):
        return self, self.tag, self.text

    def ttl(self):
        return self, self.tag, self.text, self.line

    def getvalue(self):
        return str(self)

    def cdata(self, content, safe=False):
        if safe:
            content = content.replace(']]>', ']]]]><![CDATA[>')
        super(YattagPlant, self).cdata(content)
