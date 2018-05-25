from graphics import *
# Using graphics.py for the output


def display_summary(input_data, output_pattern):
    block_length = 20
    block_width = 10
    x_border = 30
    y_border = 20
    band_length = block_length * len(output_pattern['top_cols'])
    band_width = block_width * len(input_data['Thread_colours'])
    win = GraphWin('Woven pattern', band_length + 2 * x_border, 2 * band_width + 30 + 2 * y_border
                   )
    display_output_pattern(pattern_structure=output_pattern['top_cols'],
                           prepared_window=win,
                           block_length=block_length,
                           block_width=block_width,
                           y_offset=y_border)
    display_output_pattern(pattern_structure=output_pattern['bottom_cols'],
                           prepared_window=win,
                           block_length=block_length,
                           block_width=block_width,
                           y_offset=y_border + band_width + 30)
    message = Text(Point(win.getWidth()/2, 20), 'Click anywhere to quit.')
    message.draw(win)
    win.getMouse()
    win.close()


def display_output_pattern(pattern_structure, prepared_window, block_length, block_width, y_offset):
    block_x = 20
    for pattern_row in pattern_structure:
        block_y = y_offset
        for thread in pattern_row:
            block_location = Point(block_x, block_y)
            block_end = Point(block_x + block_length, block_y + block_width)
            block = Rectangle(block_location, block_end)
            block.setFill(thread)
            block.draw(prepared_window)
            block_y += block_width
        block_x += block_length



