# coding: utf-8
# license: GPLv3
import json

from solar_model import model
from solar_vis import update_object_position, calculate_scale_factor, create_image, calculate_v_scale_factor


class SpaceBody:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселях и её цвет.
    """

    def __init__(self, type=None, m=1, x=0, y=0, vx=0, vy=0, r=5, color='red'):
        self.name = type
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
        self.vis_pt = (x, y)

        #  Tk canvas elements
        self.ids = None
        #  Body movement trace
        self.trace = [(0, x, y, vx, vy)]

    def get_state(self):
        return {
            'type': self.name,
            'm': self.m,
            'x': self.x,
            'y': self.y,
            'vx': self.vx,
            'vy': self.vy,
            'r': self.r,
            'color': self.color
        }

    def get_dist_from_last_trace(self):
        return ((self.x - self.vis_pt[0]) ** 2 +
                (self.y - self.vis_pt[1]) ** 2) ** 0.5

    def get_velocity(self):
        return (self.vx ** 2 + self.vy ** 2) ** 0.5


class Space:
    def __init__(self, canvas, trace_length):
        self.bodies = []
        self.time = 0
        self.canvas = canvas
        self.trace_length = trace_length
        self.counter = 0

    def load(self, filename):
        self.destroy_all()
        self.bodies.clear()
        configs = json.load(open(filename))
        for config in configs:
            self.bodies.append(SpaceBody(**config))
        calculate_scale_factor(self)
        calculate_v_scale_factor(self)
        for body in self.bodies:
            create_image(self.canvas, body)
            update_object_position(self, body)

    def save(self, filename):
        configs = [space_body.get_state() for space_body in self.bodies]
        json.dump(configs, open(filename, 'w'), indent=2)

    def step(self, dt):
        model(self.bodies, dt)
        self.redraw()
        self.time += dt
        if not self.counter % 25:
            for body in self.bodies:
                body.trace.append((self.time, body.x, body.y, body.vx, body.vy))
        self.counter += 1

    def redraw(self):
        for body in self.bodies:
            update_object_position(self, body)

    def destroy_all(self):
        self.canvas.delete('all')
