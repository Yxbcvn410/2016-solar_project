import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk

import matplotlib.pyplot as plt

import stats as stat


def plot(xaxis, yaxis, xtitle='', ytitle=''):
    plt.plot(xaxis, yaxis)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.show()


def show_stats(root, stats, space):
    if 0 not in stats:
        mb.showerror('Error', 'No data to plot!')
        return

    dialog = tk.Toplevel(root)

    axis_options = {'Time': lambda: stat.get_time_axis(stats)}
    for i in stats[0]:
        ii = i
        axis_options.update(
            {'Velocity of body {1}, #{0}'.format(i + 1, space.bodies[i].name): lambda: stat.get_vel_axis(stats, ii)})

    for i in stats[0]:
        for j in range(i + 1, len(stats[0])):
            ii = i
            jj = j
            axis_options.update(
                {'Distance between {2}, #{0} and {3}, #{1}'.format(i + 1, j + 1, space.bodies[i].name,
                                                                   space.bodies[j].name): lambda: stat.get_dist_axis(
                    stats, ii, jj)})

    xaxis_box = ttk.Combobox(dialog, values=list(axis_options.keys()), width=100)
    xaxis_box.set('Time')
    yaxis_box = ttk.Combobox(dialog, values=list(axis_options.keys()), width=100)
    yaxis_box.set('Time')

    show_button = tk.Button(dialog, text='Plot', command=lambda: plot(
        axis_options[xaxis_box.get()](), axis_options[yaxis_box.get()](), xaxis_box.get(), yaxis_box.get()))

    xaxis_box.pack()
    yaxis_box.pack()
    show_button.pack()
    dialog.mainloop()
