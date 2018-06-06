from tkinter import Tk, Canvas, Label, Button, N, S, E, W, Grid, filedialog
from os import path


class Interface:
    def __init__(self):
        self.rows = 100
        self.columns = 100

        self.PATTERN_DIR = path.join('..', 'Example_input_files')
        self.header_rows = 3
        self.draft_height = 4
        self.num_cards = 8
        self.length_turning_instructions = 16


        self.window = Tk()
        self.window.title("Tablet weaving design tool")

        # self.canvas.create_rectangle(20, 20, 40, 60, fill="blue")

        Label(text="Hello").grid(column=0, row=0)
        load_btn = Button(self.window, text="Load pattern", command=self.load_clicked)
        load_btn.grid(column=2 * self.length_turning_instructions + 1, row=0)
        save_btn = Button(self.window, text="Save pattern", command=self.save_clicked)
        save_btn.grid(column=2 * self.length_turning_instructions + 1, row=1)
        set_dir_btn = Button(self.window, text="Set patterns directory", command=self.set_pattern_files_location)
        set_dir_btn.grid(column=2 * self.length_turning_instructions + 1, row=2)

        draft_grid_osft = self.header_rows + 1
        turning_grid_ofst = self.header_rows + 1 + self.draft_height + 1
        output_grid_top_ofst = self.header_rows + 1 + self.draft_height + 1 + self.num_cards + 1
        output_grid_bottom_ofst = self.header_rows + 1 + self.draft_height + 1 + self.num_cards + 3

        self.make_draft_grid(x_offset=1 + int(self.length_turning_instructions - self.num_cards / 2),
                             y_offset=draft_grid_osft)
        self.make_turning_grid(x_offset=1 + int(self.length_turning_instructions / 2),
                               y_offset=turning_grid_ofst)
        self.make_output_grid(x_offset=1, y_offset=output_grid_top_ofst, tb_select='Top', data=0)
        self.make_output_grid(x_offset=1, y_offset=output_grid_bottom_ofst, tb_select='Bottom', data=0)

        self.window.mainloop()

    def save_clicked(self):
        print('Save clicked')

    def load_clicked(self):
        print('Load clicked')
        file = filedialog.askopenfilename(initialdir=self.PATTERN_DIR, filetypes=(("Pattern files", "*.json"), ("all files", "*.*")))

    def set_pattern_files_location(self):
        return filedialog.askdirectory()

    def switch_turning_direction(self, arg, squares):
        if squares[arg[0]][arg[1]].cget('bg') == 'black':
            squares[arg[0]][arg[1]].config(bg='white')
        elif squares[arg[0]][arg[1]].cget('bg') == 'white':
            squares[arg[0]][arg[1]].config(bg='black')
        else:
            raise ValueError('The button colour should be white or black')

    def make_draft_grid(self, x_offset, y_offset):
        squares = []
        Label(self.window, text="Pattern draft").grid(row=y_offset, columnspan=2 * self.length_turning_instructions)
        for x in range(self.num_cards):
            squares.append([0] * self.draft_height)
            for y in range(self.draft_height):
                squares[x][y] = Button(self.window, bg='black', command=lambda arg=(x, y): self.switch_turning_direction(arg, squares))
                squares[x][y].grid(column=x + x_offset, row=(y + y_offset + 1), sticky=(N + S + E + W))
        for x in range(self.num_cards):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.draft_height):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)

    def make_turning_grid(self, x_offset, y_offset):
        squares = []
        Label(self.window, text="Turning instructions").grid(row=y_offset,
                                                             columnspan=2 * self.length_turning_instructions)
        for x in range(self.length_turning_instructions):
            squares.append([0] * self.num_cards)
            for y in range(self.num_cards):
                squares[x][y] = Button(self.window, bg='black', command=lambda arg=(x, y): self.switch_turning_direction(arg, squares))
                squares[x][y].grid(column=x + x_offset, row=(y + y_offset + 1), sticky=(N + S + E + W))
        for x in range(self.length_turning_instructions):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.num_cards):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)

    def make_output_grid(self, x_offset, y_offset, tb_select, data):
        rect = {}
        square_size = 25  # size in pixels
        cellwidth = square_size
        cellheight = square_size
        Label(self.window, text="Output pattern (%s)" % tb_select).grid(row=y_offset,
                                                                        columnspan=2 * self.length_turning_instructions)

        canvas = Canvas(self.window, width=2 * self.length_turning_instructions * square_size,
                        height=self.num_cards * square_size, borderwidth=0, highlightthickness=0)
        canvas.grid(column=x_offset, row=y_offset + 1, columnspan=2 * self.length_turning_instructions)
        for x in range(2 * self.length_turning_instructions):
            for y in range(self.num_cards):
                x1 = x * cellwidth
                y1 = y * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                # TODO, fill=data[x, y])
                rect[x, y] = canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="rect")
        for x in range(2 * self.length_turning_instructions):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.num_cards):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)


interface1 = Interface()


