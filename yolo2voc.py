import cv2
import os
from tqdm import tqdm
import json

img_dir = 'G:/data/CV/table/datamy/images'
txt_dir = 'G:/data/CV/table/datamy/annoations'
save_path = 'xxx.json'

_txt_lists = [i for i in os.listdir(txt_dir) if i.endswith('.txt')]
img_lists = []
txt_lists = []

for txt_name in _txt_lists:
    data_name = txt_name.split('.')[0]
    for i in ['jpg', 'png', 'tif']:
        img_path = os.path.join(img_dir, f'{data_name}.{i}').replace('\\', '/')
        if os.path.exists(img_path):
            img_lists.append(f'{data_name}.{i}')
            txt_lists.append(txt_name)
            continue
            
images = []
annotations = []
categories = [{'id': 1, 'name': 'table', 'supercategory': 'table'}]  # 自行补充

m = 0
for n, img_name in enumerate(tqdm(img_lists)):
    img_path = os.path.join(img_dir, img_name).replace('\\', '/')
    txt_path = os.path.join(txt_dir, img_name.split('.')[0] + '.txt').replace('\\', '/')
    
    img = cv2.imread(img_path)
    H, W = img.shape[:2]
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        txt_data = f.read().splitlines()
    
    images.append({
                    'file_name': img_name,
                    'width': W,
                    'height': H,
                    'id': n
                    })
    
    if len(txt_data) > 0:
        for _txt_data in txt_data:
            _txt_data = _txt_data.split(' ')
            x_c, y_c, w, h = float(_txt_data[1]) * W, float(_txt_data[2]) * H, float(_txt_data[3]) * W, float(_txt_data[4]) * H
            label = int(_txt_data[0]) + 1
            x1 = round(x_c - w / 2)
            y1 = round(y_c - h / 2)
            w = round(w)
            h = round(h)
            
            annotations.append({
                                'category_id': label,
                                 'area': H * W,
                                 'iscrowd': 0,
                                 'id': m,
                                 'image_id': n,
                                 'bbox': [x1, y1, w, h]
                                })
            m += 1
            
json_data = {'images': images, 'annotations': annotations, 'categories': categories}

with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f)
