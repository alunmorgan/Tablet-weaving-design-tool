from tkinter import Tk, Canvas, Label, Button, N, S, E, W, Grid, filedialog, colorchooser, Spinbox
from os import path
import json
from graphics_weaving.static_pattern_output import regularise_turning_instructions, convert_numeric_to_colours
from from_pattern_draft.pattern_draft_to_output import convert_turns_to_numeric, accumulate_pattern


def rgb_to_tkinter_string(rgb):
    return "#%02x%02x%02x" % (round(rgb[0]), round(rgb[1]), round(rgb[2]))


def set_pattern_files_location():
    return filedialog.askdirectory()


def generate_initial_data_set(number_holes=3, number_cards=2, number_turns=8):
    data = {'Threading_directions': [],
            'Thread_colours': [],
            'Thread_types': [],
            'Turning_instructions': []
            }
    for card in range(number_cards):
        data['Threading_directions'].append('LTR')
        data['Thread_colours'].append([])
        data['Thread_types'].append([])
        for hole in range(number_holes):
            data['Thread_colours'][card].append([0, 0, 0])
            data['Thread_types'][card].append('cotton')
    for turn in range(number_turns):
        data['Turning_instructions'].append(['away'])
    return data


class Interface:
    def __init__(self):
        self.pattern_dir = path.join('..', 'Example_input_files')
        # Data structure initialisation.
        self.input_data = generate_initial_data_set()
        self.output_data = {}
        self.top_output_pattern = []
        self.bottom_output_pattern = []

        # Initial values
        self.num_holes = len(self.input_data['Thread_colours'][0])
        self.num_cards = len(self.input_data['Threading_directions'])
        self.length_turning_instructions = len(self.input_data['Turning_instructions'])
        # Interface structure initialisation.
        self.draft_grid_state = []
        self.turning_grid_state = []
        self.canvas = {}
        self.labels = {}

        self.draft_grid_osft = 0
        self.turning_grid_ofst = 0
        self.output_grid_top_ofst = 0
        self.output_grid_bottom_ofst = 0
        self.header_rows = 3

        # Creating interface.
        self.window = Tk()
        self.window.title("Tablet weaving design tool")
        self.draft_label = Label(self.window, text="Pattern draft", fg='white')
        self.turns_label = Label(self.window, text="Turning instructions", fg='white')
        welcome = Label(self.window, text="Hello", fg='white')
        welcome.grid(column=0, row=0)
        self.load_btn = Button(self.window, text="Load pattern", command=self.load_clicked)
        self.save_btn = Button(self.window, text="Save pattern", command=self.save_clicked)
        self.set_dir_btn = Button(self.window, text="Set patterns directory", command=set_pattern_files_location)
        self.cards_update_btn = Button(self.window, text="Reset with new cards settings", command=self.change_cards)
        self.num_cards_label = Label(self.window, text='number of cards', fg='white')
        self.num_cards_spinbox = Spinbox(self.window, from_=2, to=20)
        self.num_holes_label = Label(self.window, text='number of holes', fg='white')
        self.num_holes_spinbox = Spinbox(self.window, from_=3, to=8)
        self.num_turns_label = Label(self.window, text='number of turns', fg='white')
        self.num_turns_spinbox = Spinbox(self.window, from_=2, to=20)
        self.place_controls()

        self.display_input_grids()
        self.window.mainloop()

    def place_controls(self):
        self.load_btn.grid(column=2 * self.length_turning_instructions + 1, row=0)
        self.save_btn.grid(column=2 * self.length_turning_instructions + 1, row=1)
        self.set_dir_btn.grid(column=2 * self.length_turning_instructions + 1, row=2)
        self.cards_update_btn.grid(column=2 * self.length_turning_instructions + 1, row=3)
        self.num_cards_label.grid(column=2 * self.length_turning_instructions + 1, row=4)
        self.num_cards_spinbox.grid(column=2 * self.length_turning_instructions + 1, row=5)
        self.num_holes_label.grid(column=2 * self.length_turning_instructions + 1, row=6)
        self.num_holes_spinbox.grid(column=2 * self.length_turning_instructions + 1, row=7)
        self.num_turns_label.grid(column=2 * self.length_turning_instructions + 1, row=8)
        self.num_turns_spinbox.grid(column=2 * self.length_turning_instructions + 1, row=9)

    def display_input_grids(self):
        """Convenience function to create all the initial input grids."""
        self.draft_grid_osft = self.header_rows + 1
        self.turning_grid_ofst = self.header_rows + 1 + self.num_holes + 1
        self.make_draft_grid(x_offset=1 + int(self.length_turning_instructions - self.num_cards / 2),
                             y_offset=self.draft_grid_osft)
        self.make_turning_grid(x_offset=1 + int(self.length_turning_instructions / 2),
                               y_offset=self.turning_grid_ofst)

    def display_output_grids(self):
        """Convenience function to update and display both the input grids."""
        self.output_grid_top_ofst = self.header_rows + 1 + self.num_holes + 1 + self.num_cards + 1
        self.output_grid_bottom_ofst = self.header_rows + 1 + self.num_holes + 1 + self.num_cards + 3
        self.output_data = accumulate_pattern(input_data=self.input_data)
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_top_ofst, tb_select='Top')
        self.make_output_grid(x_offset=1, y_offset=self.output_grid_bottom_ofst, tb_select='Bottom')

    def save_clicked(self):
        print('Save clicked')

    def load_clicked(self):
        """Opens a file dialog and opens the selected json file. Uses the data in the file to update input_data.
        Then the existing input and output grids are cleared, and new grids are generated based on the new input data"""
        fname = filedialog.askopenfilename(initialdir=self.pattern_dir,
                                           filetypes=(("Pattern files", "*.json"), ("all files", "*.*")))
        json_file = open(fname)
        self.input_data = json.load(json_file)
        self.num_holes = len(self.input_data['Thread_colours'][0])
        self.num_cards = len(self.input_data["Threading_directions"])
        self.length_turning_instructions = len(self.input_data['Turning_instructions'])
        self.place_controls()
        self.num_cards_spinbox.selection_clear()
        self.num_cards_spinbox.selection_adjust(self.num_cards - 2)
        self.num_holes_spinbox.selection_clear()
        self.num_holes_spinbox.selection_adjust(self.num_holes - 3)
        self.num_turns_spinbox.selection_clear()
        self.num_turns_spinbox.selection_adjust(self.length_turning_instructions - 2)
        self.input_data['Turning_instructions'] = \
            regularise_turning_instructions(self.input_data['Turning_instructions'], self.num_cards)
        self.remove_draft_grid()
        self.remove_turning_grid()
        self.remove_output_grids()
        self.display_input_grids()
        self.update_draft_grid()
        self.update_turning_grid()
        self.display_output_grids()

    def change_cards(self):
        """This re initialises the grids and the input to the requested size."""
        self.input_data = generate_initial_data_set(number_holes=int(self.num_holes_spinbox.get()),
                                                    number_cards=int(self.num_cards_spinbox.get()),
                                                    number_turns=int(self.num_turns_spinbox.get()))
        self.num_holes = len(self.input_data['Thread_colours'][0])  # This seems an unnecessary variable.
        self.num_cards = len(self.input_data['Threading_directions'])
        self.length_turning_instructions = len(self.input_data['Turning_instructions'])
        self.place_controls()
        self.remove_draft_grid()
        self.remove_turning_grid()
        self.remove_output_grids()
        self.display_input_grids()
        # The stack code uses the length of Threading directions to find out the number of cards.
        self.input_data['Threading_directions'] = []
        for card in range(self.num_cards):
            self.input_data['Threading_directions'].append('LTR')
        self.display_output_grids()

    def switch_turning_direction(self, arg):
        """Flips the button between black and white. Also updates the relevant entry in input_data.
         Then regenerates the output grids.

         Args:
             arg (list of ints): The location of the button.
             """
        if self.turning_grid_state[arg[0]][arg[1]].cget('bg') == 'black':
            self.turning_grid_state[arg[0]][arg[1]].config(bg='white', text='A', fg='black')
            new_val = 'away'
        elif self.turning_grid_state[arg[0]][arg[1]].cget('bg') == 'white':
            self.turning_grid_state[arg[0]][arg[1]].config(bg='black', text='T', fg='white')
            new_val = 'toward'
        else:
            raise ValueError('The button colour should be white or black')
        self.input_data['Turning_instructions'][arg[0]][arg[1]] = new_val
        self.display_output_grids()

    def select_colour(self, arg):
        """Sets the button to the selected colour. Also updates the relevant entry in input_data.
         Then regenerates the output grids.

         Args:
             arg (list of ints): The location of the button.
             """
        # Bring up a colour selection window
        result = colorchooser.askcolor(title='Please pick a colour')
        self.draft_grid_state[arg[0]][arg[1]].config(bg=result[1])
        self.input_data['Thread_colours'][arg[0]][arg[1]] = result[0]
        self.display_output_grids()

    def make_draft_grid(self, x_offset, y_offset):
        """Initialises the draft grid of buttons. If there is no input data then an initial data set is regenerated.
        If there is no input data then an initial data set is generated.

        Args:
            x_offset (int): horizontal grid location of the start of the button grid.
            y_offset (int): vertical grid location of the start of the button grid.
        """
        self.draft_label.grid(row=y_offset, columnspan=2 * self.length_turning_instructions)
        regen_input = 0
        if 'Thread_colours' not in self.input_data.keys():
            self.input_data['Thread_colours'] = []
            self.input_data['Thread_types'] = []
            regen_input = 1
        for x in range(self.num_cards):
            if regen_input == 1:
                self.input_data['Thread_colours'].append([])
                self.input_data['Thread_types'].append([])
            self.draft_grid_state.append([0] * self.num_holes)
            for y in range(self.num_holes):
                self.draft_grid_state[x][y] = Button(self.window, bg='black',
                                                     command=lambda arg=(x, y): self.select_colour(arg))
                self.draft_grid_state[x][y].grid(column=x + x_offset, row=(y + y_offset + 1), sticky=(N + S + E + W))
                if regen_input == 1:
                    self.input_data['Thread_colours'][x].append([0, 0, 0])
                    self.input_data['Thread_types'][x].append('cotton')
        for x in range(self.num_cards):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.num_holes):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)

    def update_draft_grid(self):
        """Updates the state of each button in the pattern draft, based on data in input_data.
         Currently only change of colour."""
        new_draft = self.input_data['Thread_colours']
        for x in range(self.num_cards):
            for y in range(self.num_holes):
                self.draft_grid_state[x][y].configure(bg=rgb_to_tkinter_string(new_draft[x][y]))

    def remove_draft_grid(self):
        """Removes all buttons of the draft grid in preparation for a new one."""
        for x in range(len(self.draft_grid_state)):
            for y in range(len(self.draft_grid_state[0])):
                self.draft_grid_state[x][y].destroy()
        self.draft_grid_state = []

    def make_turning_grid(self, x_offset, y_offset):
        """Initialises the turning grid of buttons. If there is no input data then an initial data set is regenerated.
        If there is no input data then an initial data set is generated.

        Args:
            x_offset (int): horizontal grid location of the start of the button grid.
            y_offset (int): vertical grid location of the start of the button grid.
        """
        self.turns_label.grid(row=y_offset, columnspan=2 * self.length_turning_instructions)
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
                                                       self.switch_turning_direction(arg))
                self.turning_grid_state[x][y].grid(column=x + x_offset, row=(y + y_offset + 1), sticky=(N + S + E + W))
                if regen_input == 1:
                    self.input_data['Turning_instructions'][x].append('away')
        for x in range(self.length_turning_instructions):
            Grid.columnconfigure(self.window, x + x_offset, weight=1)
        for y in range(self.num_cards):
            Grid.rowconfigure(self.window, (y + y_offset + 1), weight=1)

    def update_turning_grid(self):
        """Updates the state of each button in the turning grid, based on data in input_data."""
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
        """Removes all buttons in the turning grid in preparation for a new one"""
        for x in range(len(self.turning_grid_state)):
            for y in range(len(self.turning_grid_state[0])):
                self.turning_grid_state[x][y].destroy()
        self.turning_grid_state = []

    def make_output_grid(self, x_offset, y_offset, tb_select):
        """Generate a canvas containing a grid of squares, whose colours depend upon the data in input_data.

        Args:
            x_offset (int): The horizontal location of the canvas.
            y_offset (int): The vertical location of the canvas.
            tb_select (str): Selects between the output for the top surface or the bottom surface.
            """
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
        """Removes the canvases containing the output grids, and associated labeling, if they exist."""
        if self.canvas:
            self.canvas['top'.casefold()].destroy()
            self.canvas['bottom'.casefold()].destroy()
        if self.labels:
            self.labels['top'.casefold()].destroy()
            self.labels['bottom'.casefold()].destroy()


interface1 = Interface()
