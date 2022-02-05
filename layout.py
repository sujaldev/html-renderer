from __future__ import annotations
from typing import List

from primitives import LayoutBoxBase


class LayoutBox(LayoutBoxBase):
    def __init__(self, parent: LayoutBox = None, last_sibling: LayoutBox = None, style=None):
        super().__init__(style)
        self.type = type(self)  # I find it more readable to perform type checks this way
        self.parent = parent
        self.last_sibling = last_sibling
        self.children: List[LayoutBox] = []

        self.init_box()

    def init_box(self):
        if self.parent is None:
            return
        self.inherit_parent_dimensions()

        if self.last_sibling is None:
            return
        self.position_after_last_sibling()

    # TO BE DEFINED BY CHILD CLASSES
    def inherit_parent_dimensions(self):
        pass

    def position_after_last_sibling(self):
        pass

    def add_child(self, child: LayoutBox):
        pass


class BlockBox(LayoutBox):
    def inherit_parent_dimensions(self):
        self.x1 = self.parent.x1
        self.y1 = self.parent.y1
        self.width = self.parent.width

    def position_after_last_sibling(self):
        if self.last_sibling.type is BlockBox:
            self.y1 = self.last_sibling.margin.y2
        else:
            # top and bottom margins don't work on inline boxes
            self.y1 = self.last_sibling.y2

    def add_child(self, child: LayoutBox):
        self.children.append(child)
        if child.type is BlockBox:
            self.height += child.margin.height
        else:
            self.height += child.height


class InlineBox(LayoutBox):
    def inherit_parent_dimensions(self):
        self.x1 = self.parent.x1
        self.y1 = self.parent.y1

    def position_after_last_sibling(self):
        if self.last_sibling.type is InlineBox:
            self.x1 = self.last_sibling.margin.x2
            self.y1 = self.last_sibling.y1
        else:
            self.y1 = self.last_sibling.margin.y2

    def add_child(self, child: LayoutBox):
        self.children.append(child)
