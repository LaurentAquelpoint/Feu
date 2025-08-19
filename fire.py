import numpy as np
import tkinter as tk
import random as rd

##########

n = 50
taille_pix = 20
mat_pix = np.zeros((n, n))
heat_dict = {(i, j) : "#000000" for i in range(n) for j in range(n)}
heat_matrix = np.zeros((n , n))
tempo = 10
frame_number = 100






fen = tk.Tk()
can = tk.Canvas(fen, height = taille_pix*n, width = taille_pix*n, bg = '#FFFFFF', borderwidth = 0, highlightthickness = 0)
can.grid(row = 0, column = 0)


heat0 = np.zeros((n))

for y in range(n):
    for x in range(n):
        x1 = x * taille_pix
        y1 = (n - 1 - y) * taille_pix
        x2 = (x + 1) * taille_pix
        y2 = (n - y) * taille_pix
        col = '#%02x%02x%02x' % (0, 0, 0)
        heat_dict[(x, y)] = can.create_rectangle(x1, y1, x2, y2, fill = col, width = 0)


def smooth_heat(u):
    global n
    u_extended = np.hstack((u[0], u, u[n - 1]))
    for i in range(1, n + 1):
        u[i - 1] = (u_extended[i - 1] + u_extended[i] + u_extended[i + 1]) / 3
    return u


def init_heat0():
    global n, heat0
    for i in range(len(heat0)):
        heat0[i] = min(max(0, rd.normalvariate(6, 3)), 10)
    heat0 = smooth_heat(heat0)
    heat_matrix[0, :] = heat0


def update_heat0():
    global heat0
    for i in range(len(heat0)):
        heat0[i] = min(max(0, heat0[i] + rd.normalvariate(0, 1)), 10)
    heat0 = smooth_heat(heat0)
    heat_matrix[0, :] = heat0


def next_heat_level(u):
    v = []
    for i in range(len(u)):
        c = rd.expovariate(2)
        v.append(max(u[i] - c, 0))
    return np.array(v)


def update_heat(heat, x, y):
    global heat_dict, n, heat_matrix
    heat_matrix[x, y] = heat
    col_value = int(255 * heat / 10)
    col = '#%02x%02x%02x' % (col_value, col_value, col_value)
    can.itemconfig(heat_dict[(x, y)], fill = col)


def set_heat_level(level, u):
    global heat_dict, n, heat_matrix
    if level == 0:
        heat_matrix[level, :] = u
        for i in range(len(u)):
            update_heat(u[i], i, level)

    else:
        for i in range(len(u)):

            heat = (u[i]
                + heat_matrix[max(0, i - 1), level - 1]
                + heat_matrix[min(n - 1, i + 1), level - 1]
                + heat_matrix[i, level - 1]) / 4
            
            update_heat(heat, i, level)




init_heat0()


def set_heat_levels():
    global n, heat0
    set_heat_level(0, heat0)
    next_heat = heat0.copy()

    for level in range(1, n):
        next_heat = next_heat_level(next_heat)
        set_heat_level(level, next_heat)




set_heat_levels()



def calculate_next_heat_grid():
    update_heat0()
    set_heat_levels()
    can.after(0, next_frame)

k = 0

def next_frame():
    global frame_number, k


    can.after(tempo, calculate_next_heat_grid)
        



can.after(tempo, calculate_next_heat_grid)

    



fen.mainloop()



















































































