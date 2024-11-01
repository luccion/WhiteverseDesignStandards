import re
import json
import os

def generate_enums(datapath, outputpath):
    try:
        with open(datapath, 'r', encoding='utf-8') as file:
            file_content = file.read()

        enum_pattern = re.compile(r'public enum (\w+)\s*{([^}]*)}', re.MULTILINE | re.DOTALL)
        enum_item_pattern = re.compile(r'(\w+)\s*,?\s*//.*\n', re.MULTILINE)
        enums = {}

        for enum_match in enum_pattern.finditer(file_content):
            enum_name = enum_match.group(1)
            enum_items = enum_match.group(2)
            items = enum_item_pattern.sub(r'\1\n', enum_items)
            items = items.split('\n')

            # Remove empty strings
            items = [item.strip() for item in items if item.strip()]

            enums[enum_name] = items

        output_dir = os.path.dirname(outputpath)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(outputpath, 'w', encoding='utf-8') as json_file:
            json.dump(enums, json_file, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_enums('Assets/Scripts/Enums/Enums.cs', 'Preprocessing/Outputs/Enums.json')
