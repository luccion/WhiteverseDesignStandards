import os
import csv
import json

# This script reads all CSV files in the 'Assets/Data/i18n' directory and combines them into a single JSON file.
# It will automatically prefix each ID with the filename (without the 'i18n_' prefix) to avoid conflicts.

def process_csv_file(file_path, prefix):
    data = {}

    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        headers = csv_reader.fieldnames

        if 'id' not in headers:
            raise KeyError(f"'id' column not found in {file_path}. Headers found: {headers}")

        for row in csv_reader:
            id_with_prefix = f"{prefix}_{row['id']}" if prefix else row['id']
            for lang in ['zh_CN', 'en_US', 'zh_TW', 'ja_JP']:
                if lang not in headers:
                    raise KeyError(f"'{lang}' column not found in {file_path}. Headers found: {headers}")
                if lang not in data:
                    data[lang] = {}
                data[lang][id_with_prefix] = row[lang]

    return data

def merge_data(data, new_data):
    for lang, translations in new_data.items():
        if lang not in data:
            data[lang] = {}
        data[lang].update(translations)
    return data

def main():
    input_dir = 'Assets/StreamingAssets/Data/i18n'
    output_file = 'Preprocessing/Outputs/i18n.json'
    combined_data = {}

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            prefix = filename.split('.')[0].replace('i18n_', '')
            file_path = os.path.join(input_dir, filename)
            try:
                new_data = process_csv_file(file_path, prefix)
                combined_data = merge_data(combined_data, new_data)
            except KeyError as e:
                print(f"Error processing file {file_path}: {e}")

    with open(output_file, mode='w', encoding='utf-8') as json_file:
        json.dump(combined_data, json_file, ensure_ascii=False, indent=2)
    print(f"💡Output written to {output_file} successfully.")

if __name__ == "__main__":
    main()
