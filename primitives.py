from __future__ import annotations
from typing import Dict

import skia


class Rectangle:
    def __init__(self, background=skia.AlphaTRANSPARENT):
        self.x1, self.y1 = 0, 0
        self.width, self.height = 0, 0
        self.background = background

    @property
    def x2(self):
        return self.x1 + self.width

    @property
    def y2(self):
        return self.y1 + self.height

    def paint(self, canvas: skia.Canvas):
        skia_rect = skia.Rect(self.x1, self.y1, self.x2, self.y2)
        skia_paint = skia.Paint(self.background)
        # noinspection PyTypeChecker
        canvas.drawRect(skia_rect, skia_paint)


class RelativeRectangle(Rectangle):
    # A rectangle relative to another rectangle in terms of top, right, bottom and left units.

    def __init__(self, base_box: Rectangle, direction=1, background=skia.AlphaTRANSPARENT):
        self.__base_box = base_box  # create a rectangle relative to this rectangle

        # whether to create a relative box inside (-1) the base box or to create it outside (1)
        self.__direction = direction  # (used to differentiate padding from margin and border)

        self.background = background

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0
        super().__init__(self.background)

    @property
    def x1(self):
        return self.__base_box.x1 - (self.__direction * self.left)

    @property
    def y1(self):
        return self.__base_box.y1 - (self.__direction * self.top)

    @property
    def x2(self):
        return self.__base_box.x2 + (self.__direction * self.right)

    @property
    def y2(self):
        return self.__base_box.y2 + (self.__direction * self.bottom)

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1


class LayoutBoxBase(Rectangle):
    def __init__(self, style: Dict | None):
        super().__init__()

        self.padding = RelativeRectangle(self, direction=-1)
        self.border = RelativeRectangle(self)
        self.margin = RelativeRectangle(self.border)

        self.style = style
        if self.style:
            self.apply_styles()

    def apply_styles(self):
        self.background = self.style.get("background", self.background)
        self.set_box_property_from_style(self.margin, "margin")
        self.set_box_property_from_style(self.border, "margin")
        self.set_box_property_from_style(self.padding, "margin")

    def set_box_property_from_style(self, property_object: RelativeRectangle, property_name: str):
        property_object.top = self.style.get(f"{property_name}-top")
        property_object.right = self.style.get(f"{property_name}-right")
        property_object.bottom = self.style.get(f"{property_name}-bottom")
        property_object.left = self.style.get(f"{property_name}-left")

    def paint(self, canvas: skia.Canvas):
        self.border.paint(canvas)
        super().paint(canvas)
