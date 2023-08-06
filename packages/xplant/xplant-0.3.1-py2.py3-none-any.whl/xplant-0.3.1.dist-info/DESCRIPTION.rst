XPLANT
======

Pure pythonic tree structure builder and markup language translator.
No dependencies, quite fast, pretty syntax, no templates.

- Enter tree nodes with python's context managers.
- Cast the tree to given markup, just by calling ``str`` on it.
- Enjoy 1:1 translation from python to given markup.

Basically it's suited for XML and similar markups (SVG, HTML) but it can be used
for probably any structured markup.

XML Example
-----------

.. code:: python

    from xplant import xml_plant

    x = xml_plant()
    with x.node("section_a", attribute_1=1):
        with x.node("nested_1", empty=True):
            pass
        with x.node("nested_2"):
            x.comment("Can handle also comments.")
            for number in range(3):
                x.leaf("a_number_{:02}".format(number), num=number)


Will give:

.. code:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <section_a attribute_1="1">
      <nested_1 empty="true"></nested_1>
      <nested_2>
        <!-- Can handle also comments. -->
        <a_number_00 num="0" />
        <a_number_01 num="1" />
        <a_number_02 num="2" />
      </nested_2>
    </section_a>


HTML generation Example
-----------------------
.. code:: python

    css = """
        ul.navigation {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #f2fff5;
        }
        li {
          float: left;
        }
        li a {
          display: block;
          color: white;
          text-align: center;
          padding: 14px 16px;
          text-decoration: none;
        }
        code {
            background-color: #ded;
            padding: 4px;
            border-radius: 3px;
        }
    """
    navigation = [
        ("Home", "../home.html", "red"),
        ("Things", "stuff.html", "green"),
        ("About", "../about.html", "blue"),
    ]
    text = [
        "This page has ben generated with python's <code> xplant.html.html5_plant </code>.",
        "Enjoy pure pythonic <code>1:1 python -> xml</code> translation.",
        "break",
        "Did you ever had hard times with learning <code>HTML template language</code>? ",
        "It's a crude way to mix HTML with any logics like iterators, classes, conditions.",
        "break",
        "You know what? You already have all of it (and much more) in <code>python</code>! ",
        "HTML templates is a blind alley. HTML does not miss server-side scripting.",
        "The python miss a good HTML generator not vice versa.",
    ]

    from xplant import html5_plant

    x = html5_plant()

    with x.html():
        with x.head():
            x.meta(charset="utf-8")
            x.meta(http_equiv="Content-Security-Policy")
            x.line("title", "no templates, no headache")
            # line is a helper for creating text in a xml tag
            with x.style():
                x.text(css)

        with x.body(style="margin:28px;"):
            with x.header():
                x.line("h2", "XPLANT", id="title")
                x.line("h4", "It makes good things for you")

            x.comment("HERE COMES THE NAVIGATION")
            with x.ul(id="navigation"):
                x.comment("CHECK OUT THIS LIST")
                for name, link_url, link_color in navigation:
                    with x.li():
                        with x.a(href=link_url, style="color:%s;" % link_color):
                            x.text("%s in %s" % (name, link_color))

            x.comment("HERE COMES MAIN SECTION")
            with x.main(style="margin:20px;"):
                for paragraph in text:
                    with x.p():
                        if paragraph == "break":
                            x.br()
                        else:
                            x.text(paragraph)
    print(p)

Gives such a string:

.. code:: html

    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta http-equiv="Content-Security-Policy" />
        <title>no templates, no headache</title>
        <style>
            ul.navigation {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #f2fff5;
            }
            li {
              float: left;
            }
            li a {
              display: block;
              color: white;
              text-align: center;
              padding: 14px 16px;
              text-decoration: none;
            }
            code {
                background-color: #ded;
                padding: 4px;
                border-radius: 3px;
            }
        </style>
      </head>
      <body style="margin:28px;">
        <header>
          <h2 id="title">XPLANT</h2>
          <h4>It makes good things for you</h4>
        </header>
        <!-- HERE COMES THE NAVIGATION -->
        <ul id="navigation">
          <!-- CHECK OUT THIS LIST -->
          <li><a href="../home.html" style="color:red;">Home in red</a></li>
          <li><a href="stuff.html" style="color:green;">Things in green</a></li>
          <li><a href="../about.html" style="color:blue;">About in blue</a></li>
        </ul>
        <!-- HERE COMES MAIN SECTION -->
        <main style="margin:20px;">
          <p>This page has ben generated with python's <code> xplant.html.html5_plant </code>.</p>
          <p>Enjoy pure pythonic <code>1:1 python -> xml</code> translation.</p>
          <p><br /></p>
          <p>Did you ever had hard times with learning <code>HTML template language</code>? </p>
          <p>It's a crude way to mix HTML with any logics like iterators, classes, conditions.</p>
          <p><br /></p>
          <p>You know what? You already have all of it (and much more) in <code>python</code>! </p>
          <p>HTML templates is a blind alley. HTML does not miss server-side scripting.</p>
          <p>The python miss a good HTML generator not vice versa.</p>
        </main>
      </body>
    </html>



