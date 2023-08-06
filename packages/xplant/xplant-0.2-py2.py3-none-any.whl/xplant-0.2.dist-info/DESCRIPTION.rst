XPLANT
======

Pure pythonic tree structure model builder.

- Enter tree nodes with python's contextmanagers.
- Cast the tree to given markup (basically it's suited for XML).
- Enjoy 1:1 translation from python to given markup.

Example
--------
::

    from xplant.xml import XmlPlant

    x = XmlPlant()
    with x.node("section_a", attribute_1=1):
        with x.node("nested_1", empty=True):
            pass
        with x.node("nested_2"):
            x.comment("Can handle also comments.")
            for number in range(3):
                x.leaf("a number {:02}".format(number), num=number)

    print(x)

Will give::

    <section_a attribute_1="1">
      <nested_1 empty="true"></nested_1>
      <nested_2>
        <!-- Can handle also comments. -->
        <a number 00 num="0" />
        <a number 01 num="1" />
        <a number 02 num="2" />
      </nested_2>
    </section_a>


