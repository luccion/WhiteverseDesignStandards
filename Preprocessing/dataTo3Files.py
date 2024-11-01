import csv
import os

def generate_files(input_csv, output_path, output_prefix,language_column=["zh_CN", "en_US", "zh_TW", "ja_JP"]):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        data_file = os.path.join(output_path, f"{output_prefix}.csv")
        i18n_name_file = os.path.join(output_path, f"i18n_{output_prefix}.csv")
        i18n_desc_file = os.path.join(output_path, f"i18n_d_{output_prefix}.csv")

        with open(input_csv, 'r', encoding='utf-8-sig') as csv_file, \
             open(data_file, 'w', newline='', encoding='utf-8-sig') as data_csv, \
             open(i18n_name_file, 'w', newline='', encoding='utf-8-sig') as i18n_name_csv, \
             open(i18n_desc_file, 'w', newline='', encoding='utf-8-sig') as i18n_desc_csv:

            reader = csv.reader(csv_file)
            data_writer = csv.writer(data_csv)
            i18n_name_writer = csv.writer(i18n_name_csv)
            i18n_desc_writer = csv.writer(i18n_desc_csv)

            # Write headers for all files
            headers = next(reader)
            id_column = headers[0]   

            data_writer.writerow([id_column] + headers[9:])      
            i18n_name_writer.writerow([id_column] + language_column)
            i18n_desc_writer.writerow([id_column] + language_column)

            for row in reader:
                id_value = row[0]
                name_values = row[1:5]
                desc_values = row[5:9]                
                
                data_writer.writerow([id_value] + row[9:])
                i18n_name_writer.writerow([id_value] + name_values)
                i18n_desc_writer.writerow([id_value] + desc_values)

        print(f"Files generated successfully: {data_file}, {i18n_name_file}, {i18n_desc_file}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    input_file_path = 'Preprocessing/Data/skills.csv'
    output_file_path = 'Preprocessing/Outputs/skills'
    generate_files(input_file_path, output_file_path, 'skills')
