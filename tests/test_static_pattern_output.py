from graphics_weaving.static_pattern_output import *
import unittest
from unittest.mock import MagicMock, patch


class TestDispalyOutputPattern(unittest.TestCase):
    def setUp(self):
        self.pattern_structure = [['away'], ['away'], ['away'], ['away'], ['away'], ['away'], ['away'], ['away'],
                                       ['towards'], ['towards'], ['towards'], ['towards'], ['towards'], ['towards'],
                                       ['towards'], ['towards']]
        self.prepared_window = GraphWin('TEST WINDOW', 11, 22)
        self.block_length = 555
        self.block_width = 444
        self.y_offset = 333
        self.x_offset = 222
        self.name = 'TEST'

    @patch('graphics_weaving.static_pattern_output.show_object')
    def test_display_output_pattern_does_not_error_with_expected_input(self, mock_draw):
        display_output_pattern(pattern_structure=self.pattern_structure,
                               prepared_window=self.prepared_window,
                               block_length=self.block_length,
                               block_width=self.block_width,
                               y_offset=self.y_offset,
                               x_offset=self.x_offset,
                               name=self.name)

    def test_display_output_pattern_raises_typerror_with_block_length_as_str(self):
        self.assertRaises(TypeError, display_output_pattern, pattern_structure=self.pattern_structure,
                          prepared_window=self.prepared_window, block_length='TTT',
                          block_width=self.block_width, y_offset=self.y_offset, x_offset=self.x_offset, name=self.name)

    def test_display_output_pattern_raises_typerror_with_block_width_as_str(self):
        self.assertRaises(TypeError, display_output_pattern, pattern_structure=self.pattern_structure,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width='TTT', y_offset=self.y_offset, x_offset=self.x_offset, name=self.name)

    def test_display_output_pattern_raises_typerror_with_y_offset_as_str(self):
        self.assertRaises(TypeError, display_output_pattern, pattern_structure=self.pattern_structure,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset='TTT', x_offset=self.x_offset, name=self.name)

    def test_display_output_pattern_raises_typerror_with_x_offset_as_str(self):
        self.assertRaises(TypeError, display_output_pattern, pattern_structure=self.pattern_structure,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset=self.y_offset, x_offset='TTT', name=self.name)

    def test_display_output_pattern_raises_typerror_with_name_as_numeric(self):
        self.assertRaises(TypeError, display_output_pattern, pattern_structure=self.pattern_structure,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset=self.y_offset, x_offset=self.x_offset, name=555)
        self.assertRaises(TypeError, display_output_pattern, pattern_structure=self.pattern_structure,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset=self.y_offset, x_offset=self.x_offset, name=77.77)


class TestDispalyPatternDraft(unittest.TestCase):
    def setUp(self):
        self.input_data = {'Card_number_of_holes': 4,
                           'Threading_directions': ['LTR', 'LTR', 'LTR', 'LTR', 'LTR', 'LTR', 'LTR', 'LTR'],
                           'Thread_colours': [['red', 'blue', 'yellow', 'cyan'],
                                              ['blue', 'yellow', 'cyan', 'red'],
                                              ['yellow', 'cyan', 'red', 'blue'],
                                              ['cyan', 'red', 'blue', 'yellow'],
                                              ['red', 'blue', 'yellow', 'cyan'],
                                              ['blue', 'yellow', 'cyan', 'red'],
                                              ['yellow', 'cyan', 'red', 'blue'],
                                              ['cyan', 'red', 'blue', 'yellow']
                                              ],
                           'Thread_types': [['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton'],
                                            ['cotton', 'cotton', 'cotton', 'cotton']
                                            ],
                           'Turning_instructions': [['away'], ['away'], ['away'], ['away'],
                                                    ['away'], ['away'], ['away'], ['away'],
                                                    ['towards'], ['towards'], ['towards'], ['towards'],
                                                    ['towards'], ['towards'], ['towards'], ['towards']]
                           }
        self.prepared_window = GraphWin('TEST WINDOW', 11, 22)
        self.block_length = 555
        self.block_width = 444
        self.y_offset = 333
        self.x_offset = 222
        self.name = 'TEST'

    @patch('graphics_weaving.static_pattern_output.show_object')
    def test_display_output_pattern_does_not_error_with_expected_input(self, mock_draw):
        display_pattern_draft(input_data=self.input_data,
                              prepared_window=self.prepared_window,
                              block_length=self.block_length,
                              block_width=self.block_width,
                              y_offset=self.y_offset,
                              x_offset=self.x_offset,
                              name=self.name)

    def test_display_output_pattern_raises_typerror_with_block_length_as_str(self):
        self.assertRaises(TypeError, display_pattern_draft, input_data=self.input_data,
                          prepared_window=self.prepared_window, block_length='TTT',
                          block_width=self.block_width, y_offset=self.y_offset, x_offset=self.x_offset, name=self.name)

    def test_display_output_pattern_raises_typerror_with_block_width_as_str(self):
        self.assertRaises(TypeError, display_pattern_draft, input_data=self.input_data,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width='TTT', y_offset=self.y_offset, x_offset=self.x_offset, name=self.name)

    def test_display_output_pattern_raises_typerror_with_y_offset_as_str(self):
        self.assertRaises(TypeError, display_pattern_draft, input_data=self.input_data,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset='TTT', x_offset=self.x_offset, name=self.name)

    def test_display_output_pattern_raises_typerror_with_x_offset_as_str(self):
        self.assertRaises(TypeError, display_pattern_draft, input_data=self.input_data,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset=self.y_offset, x_offset='TTT', name=self.name)

    def test_display_output_pattern_raises_typerror_with_name_as_numeric(self):
        self.assertRaises(TypeError, display_pattern_draft, input_data=self.input_data,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset=self.y_offset, x_offset=self.x_offset, name=555)
        self.assertRaises(TypeError, display_pattern_draft, input_data=self.input_data,
                          prepared_window=self.prepared_window, block_length=self.block_length,
                          block_width=self.block_width, y_offset=self.y_offset, x_offset=self.x_offset, name=77.77)


class TestRegulariseTurningInstructions(unittest.TestCase):
    def setUp(self):
        self.instructions = [['away'], ['away'], ['away'], ['away'], ['away'], ['away'], ['away'], ['away'],
                             ['towards'], ['towards'], ['towards'], ['towards'], ['towards'], ['towards'],
                             ['towards'], ['towards']]

    def test_regularise_turning_instructions_raises_TypeError_with_number_of_cards_as_a_str(self):
        self.assertRaises(TypeError, regularise_turning_instructions, self.instructions, 'TEST')

    def test_regularise_turning_instructions_raises_TypeError_with_number_of_cards_as_a_float(self):
        self.assertRaises(TypeError, regularise_turning_instructions, self.instructions, 4.444)

    def test_regularise_turning_instructions_raises_TypeError_with_instructions_as_a_str(self):
        self.assertRaises(TypeError, regularise_turning_instructions, 'TEST', 4)
    def test_regularise_turning_instructions_raises_TypeError_with_instructions_as_a_int(self):
        self.assertRaises(TypeError, regularise_turning_instructions, 11, 4)
    def test_regularise_turning_instructions_raises_TypeError_with_instructions_as_a_float(self):
        self.assertRaises(TypeError, regularise_turning_instructions, 22.222, 4)
    def test_regularise_turning_instructions_raises_TypeError_with_instructions_as_a_dict(self):
        self.assertRaises(TypeError, regularise_turning_instructions, {'TEST': 'aaaa'}, 4)


class TestConvertNumericToColours(unittest.TestCase):
    def test_convert_numeric_to_colours_returns_white_with_input_1(self):
        self.assertEquals(convert_numeric_to_colours(1), 'white')

    def test_convert_numeric_to_colours_returns_black_with_input_minus1(self):
        self.assertEquals(convert_numeric_to_colours(1), 'white')

    def test_convert_numeric_to_colours_raises_ValueError_with_input_0(self):
        self.assertRaises(ValueError, convert_numeric_to_colours, 0)

    def test_convert_numeric_to_colours_raises_TypeError_with_input_str(self):
        self.assertRaises(TypeError, convert_numeric_to_colours, '0')

    def test_convert_numeric_to_colours_raises_TypeError_with_input_float(self):
        self.assertRaises(TypeError, convert_numeric_to_colours, '1.111')


if __name__ == '__main__':
    unittest.main()