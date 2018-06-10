from tkinter import Tk, Canvas, Label, Button, N, S, E, W, Grid, filedialog, colorchooser, Spinbox
from os import path
import json
from graphics_weaving.static_pattern_output import regularise_turning_instructions, convert_numeric_to_colours
from from_pattern_draft.pattern_draft_to_output import convert_turns_to_numeric, accumulate_pattern


def rgb_to_tkinter_string(rgb):
    return "#%02x%02x%02x" % (round(rgb[0]), round(rgb[1]), round(rgb[2]))


class Interface:
    def __init__(self):
        self.pattern_dir = path.join('..', 'Example_input_files')
        self.input_data = {}
        self.output_data = {}
        self.window = Tk()
        self.window.title("Tablet weaving design tool")

        self.draft_grid_state = []
        self.turning_grid_state = []
        self.top_output_pattern = []
        self.bottom_output_pattern = []
        self.canvas = {}
        self.labels = {}

        self.draft_grid_osft = 0
        self.turning_grid_ofst = 0
        self.output_grid_top_ofst = 0
        self.output_grid_bottom_ofst = 0

        self.rows = 100
        self.columns = 100
        self.header_rows = 3
        self.draft_height = 4
        self.num_cards = 8
        self.length_turning_instructions = 16

        welcome = Label(self.window, text="Hello", fg='white')
        welcome.grid(column=0, row=0)
        load_btn = Button(self.window, text="Load pattern", command=self.load_clicked)
        load_btn.grid(column=2 * self.length_turning_instructions + 1, row=0)
        save_btn = Button(self.window, text="Save pattern", command=self.save_clicked)
        save_btn.grid(column=2 * self.length_turning_instructions + 1, row=1)
        set_dir_btn = Button(self.window, text="Set patterns directory", command=self.set_pattern_files_location)
        set_dir_btn.grid(column=2 * self.length_turning_instructions + 1, row=2)
        num_cards_label = Label(self.window, text='number of cards', fg='white')
        num_cards_label.grid(column=2 * self.length_turning_instructions + 1, row=4)
        self.num_cards_spinbox = Spinbox(self.window, from_=2, to=20)
        self.num_cards_spinbox.grid(column=2 * self.length_turning_instructions + 1, row=5)
        num_holes_label = Label(self.window, text='number of holes', fg='white')
        num_holes_label.grid(column=2 * self.length_turning_instructions + 1, row=6)
        self.num_holes_spinbox = Spinbox(self.window, from_=3, to=8)
        self.num_holes_spinbox.grid(column=2 * self.length_turning_instructions + 1, row=7)
        cards_update_btn = Button(self.window, text="Reset with new cards settings", command=self.change_cards)
        cards_update_btn.grid(column=2 * self.length_turning_instructions + 1, row=3)

        self.display_input_grids()
        self.window.mainloop()

    def display_input_grids(self):
        self.draft_grid_osft = self.header_rows + 1
        self.turning_grid_ofst = self.header_rows + 1 + self.draft_height + 1
        self.output_grid_top_ofst = self.header_rows + 1 + self.draft_height + 1 + self.num_cards + 1
        self.output_grid_bottom_ofst = self.header_rows + 1 + self.draft_height + 1 + self.num_cards + 3

        self.make_draft_grid(x_offset=1 + int(self.length_turning_instructions - self.num_cards / 2),
                             y_offset=self.draft_grid_osft)
        self.make_turning_grid(x_offset=1 + int(self.length_turning_instructions / 2),
                               y_offset=self.turning_grid_ofst)

    def display_output_grids(self):
        self.output_data = accumulate_pattern(input_data=self.input_data)
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_top_ofst, tb_select='Top')
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_bottom_ofst, tb_select='Bottom')

    def save_clicked(self):
        print('Save clicked')

    def load_clicked(self):
        fname = filedialog.askopenfilename(initialdir=self.pattern_dir,
                                           filetypes=(("Pattern files", "*.json"), ("all files", "*.*")))
        json_file = open(fname)
        self.input_data = json.load(json_file)
        self.num_cards = len(self.input_data["Threading_directions"])
        self.num_cards_spinbox.selection_clear()
        self.num_cards_spinbox.selection_adjust(self.num_cards - 2)
        self.input_data['Turning_instructions'] = \
            regularise_turning_instructions(self.input_data['Turning_instructions'], self.num_cards)
        self.remove_draft_grid()
        self.remove_turning_grid()
        self.remove_output_grids()
        self.display_input_grids()
        self.update_draft_grid()
        self.update_turning_grid()
        self.display_output_grids()

    def set_pattern_files_location(self):
        return filedialog.askdirectory()

    def change_cards(self):
        """This re initialises the grids and the input to the requested size."""
        self.num_cards = int(self.num_cards_spinbox.get())
        self.input_data = {}
        self.input_data['Card_number_of_holes'] = int(self.num_holes_spinbox.get())
        self.draft_height = self.input_data['Card_number_of_holes']  # This seems an unnecessary variable.
        self.remove_draft_grid()
        self.remove_turning_grid()
        self.remove_output_grids()
        self.display_input_grids()
        # The stack code uses the length of Threading directions to find out the number of cards.
        self.input_data['Threading_directions'] = []
        for card in range(self.num_cards):
            self.input_data['Threading_directions'].append('LTR')
        self.display_output_grids()

    def switch_turning_direction(self, arg, squares):
        if squares[arg[0]][arg[1]].cget('bg') == 'black':
            squares[arg[0]][arg[1]].config(bg='white', text='A', fg='black')
            new_val = 'away'
        elif squares[arg[0]][arg[1]].cget('bg') == 'white':
            squares[arg[0]][arg[1]].config(bg='black', text='T', fg='white')
            new_val = 'toward'
        else:
            raise ValueError('The button colour should be white or black')
        self.input_data['Turning_instructions'][arg[0]][arg[1]] = new_val
        self.output_data = accumulate_pattern(input_data=self.input_data)
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_top_ofst, tb_select='Top')
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_bottom_ofst, tb_select='Bottom')

    def select_colour(self, arg, draft):
        # Bring up a colour selection window
        result = colorchooser.askcolor(title='Please pick a colour')
        draft[arg[0]][arg[1]].config(bg=result[1])
        self.input_data['Thread_colours'][arg[0]][arg[1]] = result[0]
        self.output_data = accumulate_pattern(input_data=self.input_data)
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_top_ofst, tb_select='Top')
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_bottom_ofst, tb_select='Bottom')

    def make_draft_grid(self, x_offset, y_offset):
        """Initialises the draft grid of buttons. If there is not input data then an initial data set is regenerated."""
        Label(self.window, text="Pattern draft").grid(row=y_offset, columnspan=2 * self.length_turning_instructions)
        regen_input = 0
        if 'Thread_colours' not in self.input_data.keys():
            self.input_data['Thread_colours'] = []
            self.input_data['Thread_types'] = []
            regen_input = 1
        for x in range(self.num_cards):
            if regen_input == 1:
                self.input_data['Thread_colours'].append([])
                self.input_data['Thread_types'].append([])
            self.draft_grid_state.append([0] * self.draft_height)
            for y in range(self.draft_height):
                self.draft_grid_state[x][y] = Button(self.window, bg='black',
                                                     command=lambda arg=(x, y):
                                                     self.select_colour(arg, self.draft_grid_state))
                self.draft_grid_state[x][y].grid(column=x + x_offset, row=(y + y_offset + 1), sticky=(N + S + E + W))
                if regen_input == 1:
                    self.input_data['Thread_colours'][x].append([0, 0, 0])
                    self.input_data['Thread_types'][x].append('cotton')
        for x in range(self.num_cards):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.draft_height):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)

    def update_draft_grid(self):
        """Updates the state of a single button in the pattern draft. Currently only change of colour."""
        new_draft = self.input_data['Thread_colours']
        for x in range(self.num_cards):
            for y in range(self.draft_height):
                self.draft_grid_state[x][y].configure(bg=rgb_to_tkinter_string(new_draft[x][y]))

    def remove_draft_grid(self):
        """Removes all buttons of the draft grin in preparation for a new one."""
        for x in range(len(self.draft_grid_state)):
            for y in range(len(self.draft_grid_state[0])):
                self.draft_grid_state[x][y].destroy()
        self.draft_grid_state = []

    def make_turning_grid(self, x_offset, y_offset):
        Label(self.window, text="Turning instructions").grid(row=y_offset,
                                                             columnspan=2 * self.length_turning_instructions)
        regen_input = 0
        if 'Turning_instructions' not in self.input_data.keys():
            self.input_data['Turning_instructions'] = []
            regen_input = 1
        for x in range(self.length_turning_instructions):
            self.turning_grid_state.append([0] * self.num_cards)
            if regen_input == 1:
                self.input_data['Turning_instructions'].append([])
            for y in range(self.num_cards):
                self.turning_grid_state[x][y] = Button(self.window, bg='white', text='A', fg='black',
                                                       command=lambda arg=(x, y):
                                                       self.switch_turning_direction(arg, self.turning_grid_state))
                self.turning_grid_state[x][y].grid(column=x + x_offset, row=(y + y_offset + 1), sticky=(N + S + E + W))
                if regen_input == 1:
                    self.input_data['Turning_instructions'][x].append('away')
        for x in range(self.length_turning_instructions):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.num_cards):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)

    def update_turning_grid(self):
        for x in range(self.length_turning_instructions):
            for y in range(self.num_cards):
                bg_col = convert_numeric_to_colours(convert_turns_to_numeric(
                    self.input_data['Turning_instructions'][x][y]))
                if bg_col == 'white':
                    self.turning_grid_state[x][y].configure(bg=bg_col, text='A', fg='black')
                elif bg_col == 'black':
                    self.turning_grid_state[x][y].configure(bg=bg_col, text='T', fg='white')
                else:
                    raise ValueError('The button colour should be white or black')

    def remove_turning_grid(self):
        for x in range(len(self.turning_grid_state)):
            for y in range(len(self.turning_grid_state[0])):
                self.turning_grid_state[x][y].destroy()
        self.turning_grid_state = []

    def make_output_grid(self, x_offset, y_offset, tb_select):
        square_size = 25  # size in pixels
        cellwidth = square_size
        cellheight = square_size
        lab = Label(self.window, text="Output pattern (%s)" % tb_select)
        lab.grid(row=y_offset, columnspan=2 * self.length_turning_instructions)
        canvas = Canvas(self.window, width=2 * self.length_turning_instructions * square_size,
                        height=self.num_cards * square_size, borderwidth=0, highlightthickness=0)
        canvas.grid(column=x_offset, row=y_offset + 1, columnspan=2 * self.length_turning_instructions)
        for x in range(2 * self.length_turning_instructions):
            if tb_select.casefold() == 'top'.casefold():
                self.top_output_pattern.append([0] * self.num_cards)
            elif tb_select.casefold() == 'bottom'.casefold():
                self.bottom_output_pattern.append([0] * self.num_cards)

            for y in range(self.num_cards):
                x1 = x * cellwidth
                y1 = y * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                if tb_select.casefold() == 'top'.casefold():
                    canvas.create_rectangle(x1, y1, x2, y2,
                                            fill=rgb_to_tkinter_string(self.output_data['top_cols'][x][y]),
                                            tags="rect")
                elif tb_select.casefold() == 'bottom'.casefold():
                    canvas.create_rectangle(x1, y1, x2, y2,
                                            fill=rgb_to_tkinter_string(self.output_data['bottom_cols'][x][y]),
                                            tags="rect")
                else:
                    raise ValueError('There are only top and bottom patterns')

        for x in range(2 * self.length_turning_instructions):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.num_cards):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)
        self.canvas[tb_select.casefold()] = canvas
        self.labels[tb_select.casefold()] = lab

    def remove_output_grids(self):
        if self.canvas:
            self.canvas['top'.casefold()].destroy()
            self.canvas['bottom'.casefold()].destroy()
        if self.labels:
            self.labels['top'.casefold()].destroy()
            self.labels['bottom'.casefold()].destroy()


interface1 = Interface()
