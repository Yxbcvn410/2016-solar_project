# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие графические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 800
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = 100000  # XXX
v_scale_factor = 30000  # TODO(fetisu): Этот параметр отвечает за отображение вектора скорости. Подбери норм значение
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""


def calculate_scale_factor(space):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    global scale_factor
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space.bodies])
    scale_factor = 0.4 * min(window_height, window_width) / max_distance
    print('Scale factor:', scale_factor)


def create_image(space, space_body):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    """

    x = int(space_body.x * scale_factor) + window_width // 2
    y = int(space_body.y * scale_factor) + window_height // 2
    vx = space_body.vx * scale_factor * v_scale_factor
    vy = space_body.vy * scale_factor * v_scale_factor
    r = space_body.r
    space_body.ids = {'ball': space.create_oval([x - r, y - r], [x + r, y + r], fill=space_body.color),
                      'arrow_body': space.create_line((x, y), (x + vx, y + vy), fill=space_body.color),
                      'trace': None
                      # TODO(fetisu): Дорисуешь стрелку? Сделаешь отрисовку траектории?
                      }


def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.

    Параметры:

    **space** — холст для рисования.
    **system_name** — название системы тел.
    """
    space.create_text(30, 80, tag="header", text=system_name, font=header_font)


def update_object_position(space, space_body):
    """Перемещает отображаемый объект на холсте.

    Параметры:

    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    """
    x = int(space_body.x * scale_factor) + window_width // 2
    y = int(space_body.y * scale_factor) + window_height // 2
    vx = space_body.vx * scale_factor * v_scale_factor
    vy = space_body.vy * scale_factor * v_scale_factor
    r = space_body.r
    space.coords(space_body.ids['ball'], x - r, y - r, x + r, y + r)
    space.coords(space_body.ids['arrow_body'], x, y, x + vx, y + vy)
    #  TODO(fetisu): И здесь тоже сделай отрисовку траектории
    #   Можно ещё сделать автоматическую настройку масштаба - метод calculate_scale_factor в помощь


if __name__ == "__main__":
    print("This module is not for direct call!")
