from graphics import Point, Text, Rectangle, GraphWin, color_rgb
# Using graphics.py for the output


def display_summary(input_data, output_pattern):
    block_length = 20
    block_width = 10
    x_border = 30
    y_border = 20
    band_length = block_length * len(output_pattern['top_cols'])
    band_width = block_width * len(input_data['Thread_colours'])
    draft_height = block_width * input_data['Card_number_of_holes']
    window_width = band_length + 2 * x_border + 20
    window_height = 3 * (band_width + 30) + draft_height + 30 + 2 * y_border
    win = GraphWin('Woven pattern', window_width, window_height)

    display_pattern_draft(input_data=input_data,
                          prepared_window=win,
                          block_length=block_length,
                          block_width=block_width,
                          y_offset=y_border,
                          x_offset=window_width / 2 - (block_length * len(input_data['Thread_colours'])) / 2,
                          name='Pattern draft')
    turning_instructions = regularise_turning_instructions(input_data['Turning_instructions'],
                                                           len(input_data['Thread_colours']))
    display_output_pattern(pattern_structure=turning_instructions,
                           prepared_window=win,
                           block_length=block_length,
                           block_width=block_width,
                           y_offset=y_border + draft_height + 30,
                           x_offset=x_border,
                           name='Turning instructions')
    display_output_pattern(pattern_structure=output_pattern['top_cols'],
                           prepared_window=win,
                           block_length=block_length,
                           block_width=block_width,
                           y_offset=y_border + draft_height + 30 + band_width + 30,
                           x_offset=x_border,
                           name='Top pattern')
    display_output_pattern(pattern_structure=output_pattern['bottom_cols'],
                           prepared_window=win,
                           block_length=block_length,
                           block_width=block_width,
                           y_offset=y_border + draft_height + 30 + band_width + 30 + band_width + 30,
                           x_offset=x_border,
                           name='Bottom pattern'
                           )

    message = Text(Point(win.getWidth()/2, win.getHeight() - 10), 'Click anywhere to quit.')
    message.draw(win)
    win.getMouse()
    win.close()


def display_output_pattern(pattern_structure, prepared_window, block_length, block_width, y_offset, x_offset, name):
    if not isinstance(block_length, int) and not isinstance(block_length, float):
        raise TypeError('block length must be a number')
    if not isinstance(block_width, int) and not isinstance(block_width, float):
        raise TypeError('block width must be a number')
    if not isinstance(y_offset, int) and not isinstance(y_offset, float):
        raise TypeError('y_offset must be a number')
    if not isinstance(x_offset, int) and not isinstance(x_offset, float):
        raise TypeError('x_offset must be a number')
    if not isinstance(name, str):
        raise TypeError('name need to be a string')
    block_x = x_offset
    for pattern_row in pattern_structure:
        block_y = y_offset
        for thread in pattern_row:
            block_location = Point(block_x, block_y)
            block_end = Point(block_x + block_length, block_y + block_width)
            block = Rectangle(block_location, block_end)
            if isinstance(thread, list):
                block.setFill(color_rgb(r=thread[0], g=thread[1], b=thread[2]))
            else:
                col_vals = convert_timing_instruction_to_colour(thread)
                block.setFill(color_rgb(r=col_vals[0], g=col_vals[1], b=col_vals[2]))

            show_object(block, prepared_window)
            block_y += block_width
        block_x += block_length
    message_top_pattern = Text(Point(prepared_window.getWidth() / 2, y_offset - 10), name)
    message_top_pattern.setTextColor("white")
    show_object(message_top_pattern, prepared_window)


def display_pattern_draft(input_data, prepared_window, block_length, block_width, y_offset, x_offset, name):
    if not isinstance(block_length, int) and not isinstance(block_length, float):
        raise TypeError('block length must be a number')
    if not isinstance(block_width, int) and not isinstance(block_width, float):
        raise TypeError('block width must be a number')
    if not isinstance(y_offset, int) and not isinstance(y_offset, float):
        raise TypeError('y_offset must be a number')
    if not isinstance(x_offset, int) and not isinstance(x_offset, float):
        raise TypeError('x_offset must be a number')
    if not isinstance(name, str):
        raise TypeError('name need to be a string')
    block_x = x_offset
    for draft_row in input_data['Thread_colours']:
        block_y = y_offset
        for thread in draft_row:
            block_location = Point(block_x, block_y)
            block_end = Point(block_x + block_length, block_y + block_width)
            block = Rectangle(block_location, block_end)
        #    print(thread)
#            col_vals = convert_timing_instruction_to_colour(thread)
            block.setFill(color_rgb(r=thread[0], g=thread[1], b=thread[2]))
            show_object(block, prepared_window)
            block_y += block_width
        block_x += block_length
    message_pattern_draft = Text(Point(prepared_window.getWidth() / 2, y_offset - 10), name)
    message_pattern_draft.setTextColor("white")
    show_object(message_pattern_draft, prepared_window)


def regularise_turning_instructions(input_instructions, number_of_cards):
    """ If a turning instruction is just away or toward then is applies to all cards.
        Otherwise the instruction should be a list of length number of cards.
        This function expands the single value instructions to be lists of length number of cards so that all
        entries have the same shape."""
    if not isinstance(number_of_cards, int):
        raise TypeError('number of cards needs to be an int')
    if not isinstance(input_instructions, list):
        raise TypeError('input_instructions should be a list of lists.')
    regularised_output = []
    for instruction in input_instructions:
        if len(instruction) == 1:
            output_value = instruction[0]
            temp_instruction = []
            for n_card in range(number_of_cards):
                temp_instruction.append(output_value)
            regularised_output.append(temp_instruction)
        elif len(instruction) == number_of_cards:
            regularised_output.append(instruction)
        else:
            raise ValueError('The number of turning instructions does not match the number of cards.')
    return regularised_output


def convert_numeric_to_colours(input_number):
    if not isinstance(input_number, int):
        raise TypeError('Input to convert numeric to colours needs to be an int.')
    if input_number == 1:
        return 'white'
    elif input_number == -1:
        return 'black'
    else:
        raise ValueError('Error in turn instructions (conversion)')


def convert_timing_instruction_to_colour(instruction):
    """Changes the strings to be white for away and black for towards"""
    if not isinstance(instruction, str):
        raise TypeError('Input to convert timing instruction to colour needs to be an str.')
    if instruction == 'away':
        return [255, 255, 255]
    elif instruction == 'towards':
        return [0, 0, 0]
    else:
        raise ValueError('Error in converting turn instructions to colours')


def show_object(obj, window):
    obj.draw(window)
