# coding: utf-8
# license: GPLv3
import json

from solar_model import model
from solar_vis import update_object_position, calculate_scale_factor, create_image


class SpaceBody:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселях и её цвет.
    """

    def __init__(self, type=None, m=1, x=0, y=0, vx=0, vy=0, r=5, color='red'):
        self.type = type  # TODO(fetisu): Возможно, бесполезное поле. Если да - выпили
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color

        #  Tk canvas elements
        self.ids = None
        #  Body movement trace
        self.trace = [(self.x, self.y)]

    def get_state(self):
        return {
            'type': self.type,
            'm': self.m,
            'x': self.x,
            'y': self.y,
            'vx': self.vx,
            'vy': self.vy,
            'r': self.r,
            'color': self.color
        }

    def destroy(self):
        pass  # TODO(fetisu): Убираем tk-формы с холста


class Space:
    def __init__(self, canvas):
        self.bodies = []
        self.time = 0
        self.canvas = canvas

    def load(self, filename):
        for body in self.bodies:
            body.destroy()
        self.bodies.clear()
        configs = json.load(open(filename))
        for config in configs:
            self.bodies.append(SpaceBody(**config))
        calculate_scale_factor(self)
        for body in self.bodies:
            create_image(self.canvas, body)

    def save(self, filename):
        configs = [space_body.get_state() for space_body in self.bodies]
        json.dump(configs, open(filename, 'w'), indent=2)

    def step(self, dt):
        model(self.bodies, dt)
        self.redraw()
        self.time += dt

    def redraw(self):
        for body in self.bodies:
            update_object_position(self.canvas, body)
