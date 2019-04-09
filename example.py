from from_pattern_draft.pattern_draft_to_output import accumulate_pattern, import_data
from graphics_weaving import static_pattern_output

INPUT_DATA = import_data('Example_input_files', 'basic_test_pattern')
print(INPUT_DATA)
output_pattern = accumulate_pattern(input_data=INPUT_DATA)
static_pattern_output.display_summary(output_pattern=output_pattern, input_data=INPUT_DATA)
