from from_pattern_draft.pattern_draft_to_output import Stack, accumulate_pattern, convert_turns_to_numeric
from graphics_weaving import static_pattern_output


INPUT_DATA = {'Card_number_of_holes': 4,
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
              'Turning_instructions': [['away'], ['away'], ['away'], ['away'], ['away'], ['away'], ['away'], ['away'],
                                       ['towards'],['towards'],['towards'],['towards'],['towards'],['towards'],
                                       ['towards'],['towards']]
              }

output_pattern = accumulate_pattern(input_data=INPUT_DATA)

static_pattern_output.display_summary(output_pattern=output_pattern, input_data=INPUT_DATA)