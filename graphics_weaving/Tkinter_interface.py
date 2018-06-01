from tkinter import *
from tkinter import filedialog
from os import path


def save_clicked():
    print('Save clicked')


def load_clicked():
    print('Load clicked')
    file = filedialog.askopenfilename(initialdir=PATTERN_DIR, filetypes=(("Pattern files", "*.json"), ("all files", "*.*")))


def set_pattern_files_location():
    return filedialog.askdirectory()


def switch_turning_direction(btn):
    btn.bg


def click_toggle(arg, squares):
    if squares[arg[0]][arg[1]].cget('bg') == 'black':
        squares[arg[0]][arg[1]].config(bg='white')
    elif squares[arg[0]][arg[1]].cget('bg') == 'white':
        squares[arg[0]][arg[1]].config(bg='black')
    else:
        raise ValueError('The button colour should be white or black')


def make_button_grid(win, width, height, x_offset, y_offset):
    squares = []
    for x in range(width):
        squares.append([0] * height)
        for y in range(height):
            squares[x][y] = Button(win, bg='black', command=lambda arg=(x, y): click_toggle(arg, squares))
            squares[x][y].grid(column=x + x_offset, row=(y + y_offset + 1), sticky=(N + S + E + W))
    for x in range(width):
        Grid.columnconfigure(win, x + x_offset, weight=1)
    for y in range(height):
        Grid.rowconfigure(win, (y + y_offset + 1), weight=1)


PATTERN_DIR = path.join('..', 'Example_input_files')
header_rows = 3
draft_height = 4
num_cards = 8
length_turning_instructions = 16

window = Tk()
window.geometry('%dx%d' % ((2 * length_turning_instructions) * 30 + 20,
                           (header_rows + 1 + draft_height + 2 * (1 + num_cards)) * 30))
window.title("Tablet weaving design tool")
lbl = Label(window, text="Hello")
lbl.grid(column=0, row=0)
load_btn = Button(window, text="Load pattern", command=load_clicked)
load_btn.grid(column=2 * length_turning_instructions + 1, row=0)
save_btn = Button(window, text="Save pattern", command=save_clicked)
save_btn.grid(column=2 * length_turning_instructions + 1, row=1)
set_dir_btn = Button(window, text="Set patterns directory", command=set_pattern_files_location)
set_dir_btn.grid(column=2 * length_turning_instructions + 1, row=2)


make_button_grid(win=window, width=num_cards, height=draft_height,
                 x_offset=1 + int(length_turning_instructions - num_cards / 2), y_offset=header_rows + 1)
Label(window, text="").grid(row=header_rows + 1 + draft_height + 1)
make_button_grid(win=window, width=length_turning_instructions, height=num_cards,
                 x_offset=1 + int(length_turning_instructions / 2),
                 y_offset=header_rows + 1 + draft_height + 1)
Label(window, text="").grid(row=header_rows + 1 + draft_height + 1 + num_cards + 1)
make_button_grid(win=window, width=2 * length_turning_instructions, height=num_cards, x_offset=1,
                 y_offset=header_rows + 1 + draft_height + 1 + num_cards + 1)
Label(window, text="").grid(row=header_rows + 1 + draft_height + 2 * (1 + num_cards) + 1)
make_button_grid(win=window, width=2 * length_turning_instructions, height=num_cards, x_offset=1,
                 y_offset=header_rows + 1 + draft_height + 1 + 3 * (1 + num_cards) + 1)
Label(window, text="").grid(row=header_rows + 1 + draft_height + 1 + num_cards)


window.mainloop()
