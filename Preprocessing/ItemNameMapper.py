# 读取csv表格，读取其中的中文名，将目标文件夹中的文件名改为中文名对应的id
import os
import csv

def MapItemName(csv_file, target_folder):
    # 读取 CSV 文件，获取中文名和 ID 的映射
    name_id_map = {}
    with open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过表头
        for row in reader:
            name_id_map[row[0]] = row[1]

    # 初始化计数器和列表
    matched_count = 0
    unmatched_count = 0
    matched_files = []
    unmatched_files = []

    # 遍历目标文件夹中的所有文件
    for filename in os.listdir(target_folder):
        # 获取文件名（不包括扩展名）
        filename_without_ext = os.path.splitext(filename)[0]

        # 如果文件名在映射中，就将其重命名为对应的 ID，并增加符合的计数
        if filename_without_ext in name_id_map:
            new_filename = name_id_map[filename_without_ext] + os.path.splitext(filename)[1]
            os.rename(os.path.join(target_folder, filename), os.path.join(target_folder, new_filename))
            matched_count += 1
            matched_files.append(filename)
        else:
            unmatched_count += 1
            unmatched_files.append(filename)

    # 输出报告
    print(f'Matched files: {matched_count}')
    print(matched_files)
    print(f'Unmatched files: {unmatched_count}')
    print(unmatched_files)

# 指定 CSV 文件和目标文件夹
csv_file = 'Preprocessing/Data/item_name.csv'
target_folder = 'Preprocessing/Images'

MapItemName(csv_file, target_folder)