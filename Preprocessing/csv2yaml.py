import pandas as pd
import yaml

# 注意要创建好creatures.yaml目标文件，不然会报错。

def csv_to_yaml(csv_file, yaml_file):
    # 读取CSV文件
    data = pd.read_csv(csv_file)
    
    # 将DataFrame转换为字典列表
    data_dict = data.to_dict(orient='records')
    
    # 将字典列表写入YAML文件
    with open(yaml_file, 'w', encoding='utf-8') as file:
        yaml.dump(data_dict, file, allow_unicode=True, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    input_csv = 'Preprocessing/Data/creatures.csv'
    output_yaml ='Preprocessing/Outputs/creatures.yaml'
    csv_to_yaml(input_csv, output_yaml)
    print(f"YAML file generated successfully: {output_yaml}")
