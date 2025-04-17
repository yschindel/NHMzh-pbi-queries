import json
import csv
import os

def get_parent_text(code_dict, code):
    # Get text for single letter (e.g., 'A' from 'A01.01')
    letter = code[0]
    letter_text = code_dict.get(letter, '')
    
    # Get text for number before dot (e.g., 'A01' from 'A01.01')
    parts = code.split('.')
    if len(parts) == 1 and len(parts[0]) != 1:
        number_code = parts[0]
        number_text_1 = code_dict.get(number_code, '')
        number_text_2 = ''
    elif len(parts) == 2:
        number_code = parts[0]
        number_text_1 = code_dict.get(number_code, '')
        number_text_2 = code_dict.get(code, '')
    else:
        number_text_1 = ''
        number_text_2 = ''
    return letter_text, number_text_1, number_text_2

def process_cost_codes(input_json, output_csv):
    # Read JSON file
    with open(input_json, 'r', encoding='utf-8') as f:
        code_dict = json.load(f)
    
    # Write CSV file
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['code', 'text_letter', 'text_number1', 'text_number2'])
        
        # Process each code
        for code, description in code_dict.items():
            letter_text, number_text_1, number_text_2 = get_parent_text(code_dict, code)
            writer.writerow([code, letter_text, number_text_1, number_text_2])

if __name__ == '__main__':
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output paths relative to the script location
    input_json = os.path.join(script_dir, 'cost_codes.json')
    output_csv = os.path.join(script_dir, 'cost_codes.csv')
    
    process_cost_codes(input_json, output_csv)
    print(f"CSV file has been created at: {output_csv}") 