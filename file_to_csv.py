import ast
import csv
import re

def extract_lists_from_python_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Use regex to find all lists in the content
    list_pattern = re.compile(r'(\w+)\s*=\s*\[(.*?)\]', re.DOTALL)
    lists = list_pattern.findall(content)
    
    extracted_data = {}
    
    for name, list_content in lists:
        # Fix potential trailing commas
        list_content = re.sub(r',\s*\]', ']', list_content)
        list_content = '[' + list_content + ']'
        
        try:
            parsed_list = ast.literal_eval(list_content)
            if isinstance(parsed_list, list):
                extracted_data[name] = parsed_list
            else:
                print(f"Error: {name} is not a list.")
        except Exception as e:
            print(f"Error parsing list {name}: {e}")
            extracted_data[name] = []
    
    return extracted_data

def write_lists_to_csv(lists_dict, csv_file_path):
    # Get the maximum length of the lists
    max_length = max(len(lst) for lst in lists_dict.values())
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the headers
        headers = lists_dict.keys()
        writer.writerow(headers)
        
        # Write the rows
        for i in range(max_length):
            row = [lists_dict[key][i] if i < len(lists_dict[key]) else '' for key in lists_dict]
            writer.writerow(row)

# Example usage
python_file_path = '/home/farhod/PC/2024/AP_Ps/P_2/code/prompts.py'  # Replace with the path to your Python file
csv_file_path = 'output.csv'  # Output CSV file

lists_dict = extract_lists_from_python_file(python_file_path)
write_lists_to_csv(lists_dict, csv_file_path)
