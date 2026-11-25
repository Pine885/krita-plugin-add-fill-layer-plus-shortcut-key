import re

BASE_NAME = "Fill Layer"
_NUMBERED_NAME = re.compile(r".* (\d+)$")


def next_layer_name(existing_names, base=BASE_NAME):
    """Return the next layer name using Krita's numbered-name convention."""
    names = [str(name) for name in existing_names]

    if len(names) == 1:
        return "Background"

    highest = 0
    for name in names:
        match = _NUMBERED_NAME.match(name)
        if match:
            highest = max(highest, int(match.group(1)))
    return "%s %d" % (base, highest + 1)


def insertion_point(active, root):
    """Return (parent, above) for a new layer, matching Krita's placement."""
    if active is None:
        return root, None
    if active.type() == "grouplayer":
        if not active.collapsed():
            return active, None
        return _parent_above(active)

    return _parent_above(active)


def _parent_above(node):
    above = node
    parent = node.parentNode()
    while parent is not None and parent.type() != "grouplayer":
        above = parent
        parent = parent.parentNode()
    return parent, above
