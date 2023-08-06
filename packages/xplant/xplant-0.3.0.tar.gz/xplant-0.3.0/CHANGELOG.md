## 0.1 Initial version

Its engine is under extraction from `yawrap` in order to make it a standalone library.

## 0.2 Giving the sketches form closer to maturity

The package gets shapes of final version.
`XPlant` is a proxy for exposing given node type interface.
`XML` and basic `YAML` markups are supported.

### 0.2.1 Extending functionality
- Redefining tox test environment 
- Accommodation of gitlab's pipelines config
- Adding SvgPlant and HtmlPlant

## 0.3.0 XPlant is not a class anymore
It became just a name. All its functionality as been shifted to `NodeBase` class.
Before this change we needed to have a class that creates a root node, holds nodes stack
and forwards access to top node attributes. It was kindly dispatching getattr
calls to nodes according to current python's scope i.e. context of current node.

- In 0.3 it behaves in the same way (from usage point of view), but `NodeBase`
class cares for that itself (took XPlant responsibility).
Advantage of that is less scripting in order to create a new schema/markup language.

- Another (huge) advantage of aspect mentioned above is that you can *crossbred* node types 
in the same plant structure! E.g. having a HTML plant and you can grow up SVG plant 
on top of one (or many) of HTML's plant branches.

- XPlant becomes a function that returns initialized root node instance. In order to conform 
`PEP8` the main-entry all the names changed e.g. from `XmlPlant` to `xml_plant`.

- Adding automatic `xmlns` attribute names substitution from e.g. `xmlns_blabla` to `xmlns:blabla`.
That allows for much easier keyword-argument usage in node creation.

- Root node is not a separate (derived) class anymore. Root functionality is gained 
by creating instance of regular node without passing parent handle to it.
I.e. root is a node that has no parents.
