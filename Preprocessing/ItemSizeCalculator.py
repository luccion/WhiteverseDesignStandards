# 通过读取文件夹中的图片和文件名，计算每个图片的占用16x16的格子的长宽，然后将其存储到csv中
import os
from PIL import Image
import csv

def CalculateItemSize(image_folder,output_csv):
    # 创建一个列表来存储结果
    results = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(image_folder):
        # 检查文件是否是图片
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # 打开图片并获取其尺寸
            image = Image.open(os.path.join(image_folder, filename))
            width, height = image.size
            # 计算图片占用的 16x16 格子的长宽
            grid_x = ((width + 15) // 16) 
            grid_y = ((height + 15) // 16)
            # 将结果添加到列表中
            results.append([os.path.splitext(filename)[0], grid_x, grid_y])

    # 将结果写入 CSV 文件
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['filename', 'grid_count'])  # 写入表头
        writer.writerows(results)  # 写入数据

# 指定图片文件夹和输出的 CSV 文件
image_folder = 'Preprocessing/Images'
output_csv = 'Preprocessing/Outputs/output.csv'
CalculateItemSize(image_folder,output_csv)
