import json
import os
from tqdm import tqdm

classes = open('classes.txt', 'r', encoding='utf-8').read().splitlines()
local_path = '/home/disk3/data/'
label_dir = './doclay_train_val'
label_studio_data_path = "F:\downloads\project-22-at-2024-06-21-02-37-764a3207.json"

if not os.path.exists(label_dir):
    os.makedirs(label_dir, exist_ok=True)

classes_dict = {}
for n, v in enumerate(classes):
    classes_dict[v] = str(n)

label_studio_data = json.load(open(label_studio_data_path))

for _data in tqdm(label_studio_data):
    label_data = []
    image_path = _data['image'].replace('/data/local-files/?d=', local_path)
    image_name = '.'.join(image_path.split('/')[-1].split('.')[:-1])
    save_path = os.path.join(label_dir, image_name + '.txt').replace('\\', '/')

    for _label in _data['label']:
        block_label = classes_dict[_label['rectanglelabels'][0]]
        x = _label['x']
        y = _label['y']
        width = _label['width']
        height = _label['height']

        original_width = _label['original_width']
        original_height = _label['original_height']

        _xc = (x + width / 2) / 100
        _yc = (y + height / 2) / 100
        _w = width / 100
        _h = height / 100

        label_data.append(' '.join([block_label, str(_xc), str(_yc), str(_w), str(_h)]))
    
    with open(save_path, 'w', encoding='utf-8') as f:
        for _d in label_data:
            f.write(_d)
            f.write('\n')
