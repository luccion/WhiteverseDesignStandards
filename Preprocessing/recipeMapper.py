
# 使用方法：
# 1. 将recipe.csv和item_name.csv放在Preprocessing/Data文件夹下
# 2. 注意在生成csv时，使用记事本等编辑器将编码重新调整为utf-8-sig
# 3. item_name.csv中的第一列为物品名称,第二列为物品ID
import csv
import yaml   
import os
  
def convert_to_yaml(data1, data2):
     # 读取数据组2并转换为映射关系字典
    with open(data2, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        item_map = {rows[0]: rows[1] for rows in reader}
    output_inputs = []
    # 读取数据组1,除了内容为"<"或">"的项，所有奇数索引项都映射为item_map中的值
    with open(data1, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)        
        for row in reader:               
            for i in range(len(row)):
                if row[i] == '':
                   row[i] = '0'    
                if row[i] == '<' or row[i] == '>':
                   continue
                if i % 2 == 1 and i >1:                    
                    row[i] = ','.join(map(lambda x: item_map.get(x, x), row[i].split(',')))    
            output_inputs.append(row)
    
    yaml_data = []
    k = 0
    for row in output_inputs:
        k += 1
        direction = 'Forward'

        for s in row:     
            i += 1       
            if s == '<':
                direction = 'Backward'
                break
            elif s == '>':
                direction = 'Forward'
                break 
        leftItemIndex =0
        rightItemIndex =0
        # 检测左侧物品的数量，通过检测第一个“>”或“<”之前的数字来确定
        for i in range(len(row)):
            if row[i] == '<' or row[i] == '>':
                leftItemIndex = i
                rightItemIndex = i+2
                break
        craftMethodIndex = 0
        timeCostIndex = 1               
        
        # 从左侧的物品列表中提取物品和数量，这里的row[2:leftItemIndex]其实是[2, leftItemIndex-1]的区间
        leftItems = row[2:leftItemIndex]
        newLeftItems = []
        for i in range(0, len(leftItems), 2):
            if leftItems[i] == '0':
                continue
            newLeftItems.append({leftItems[i+1]:leftItems[i]}) 
       
        rightItems = row[rightItemIndex:]        

        # 从右侧物品中提取物品和催化剂，催化剂标记为##
        newRightItems = []
        catalystList = []
        for i in range(0, len(rightItems), 2):
            if rightItems[i] == '0':
                continue
            if rightItems[i] == '##':
                catalystList = rightItems[i+1].split(',')
                break
            newRightItems.append({rightItems[i+1]:rightItems[i]}) 

        yaml_item ={ 
                'Output':[],
                'Input': [],
                'CatalystList': list(map(int, catalystList)),
                'CraftMethod':row[craftMethodIndex], 
                'TimeCost':int(row[timeCostIndex]),               
            }        
        def add_items(newItems, yaml_item, key):
            for i in range(len(newItems)):                
                item = {
                    'Id': list(map(int, list(newItems[i].keys())[0].split(','))),
                    'Count': int(list(newItems[i].values())[0])
                }
                yaml_item[key].append(item)
        if direction == 'Forward':
            add_items(newLeftItems, yaml_item, 'Input')
            add_items(newRightItems, yaml_item, 'Output')
        else:
            add_items(newLeftItems, yaml_item, 'Output')
            add_items(newRightItems, yaml_item, 'Input')
        yaml_data.append(yaml_item)
    return yaml_data    
   
theyaml = convert_to_yaml('Preprocessing/Data/recipe.csv', 'Preprocessing/Data/item_name.csv')
output_path = 'Preprocessing/Outputs/recipe.yaml'
yaml.Dumper.ignore_aliases = lambda *args : True
if not os.path.exists(output_path):
    os.makedirs(output_path)
with open(output_path, 'w', encoding='utf-8') as file:
    yaml.dump(theyaml, file, allow_unicode=True, default_flow_style=False,default_style=False, sort_keys=False)
    print('YAML file has been created successfully.')

