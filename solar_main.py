# coding: utf-8
# license: GPLv3

import tkinter.filedialog

from solar_vis import window_width, window_height
from space import Space

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space = None


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global space
    global displayed_time
    try:
        space.step(time_step.get())
    except tkinter.TclError:
        pass

    if space.time > 1000 * 365.25 * 24 * 60 * 60:
        displayed_time.set("{:e} years gone".format(space.time // (365.25 * 24 * 60 * 60)))

    elif space.time > 365.25 * 24 * 60 * 60:
        displayed_time.set("{:.0f} years and {:.0f} days gone".format(space.time // (365.25 * 24 * 60 * 60),
                                                                      (space.time // (24 * 60 * 60) % 365.25)))
    elif space.time > 24 * 60 * 60:
        displayed_time.set("{:.0f} days and {:.0f} hours gone".format(space.time // (24 * 60 * 60),
                                                                      (space.time // 3600) % 24))
    elif space.time > 3600:
        displayed_time.set("{:.0f} hours and {:.0f} min gone".format(space.time // 3600,
                                                                     (space.time // 60) % 60))
    else:
        displayed_time.set("{:.0f} min and {:.0f} seconds gone".format(space.time // 60,
                                                                       space.time % 60))

    if perform_execution:
        # TODO(fetisu): Сделай больше диапазон управления задержкой, с возможностью отключить задержку вообще
        space_canvas.after(100 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space
    stop_execution()
    in_filename = tkinter.filedialog.askopenfilename(filetypes=(("JSON file", ".json"),))
    space.load(in_filename)


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space
    out_filename = tkinter.filedialog.asksaveasfilename(filetypes=(("JSON file", ".json"),))
    if out_filename != '':
        space.save(out_filename)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global displayed_time
    global time_step
    global time_speed
    global space_canvas
    global start_button
    global space

    print('Modelling started!')

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    space_canvas = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space_canvas.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set("0 seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    trace_length = tkinter.DoubleVar()
    update_trace = tkinter.Scale(frame, variable=trace_length, orient=tkinter.HORIZONTAL)
    update_trace.pack(side=tkinter.RIGHT)

    space = Space(space_canvas, trace_length)

    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()
