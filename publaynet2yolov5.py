import json
import os
import shutil
from tqdm import tqdm

to_dir = './'
img_dir = './images'
label_dir = './labels'

os.makedirs(img_dir, exist_ok = True)
os.makedirs(label_dir, exist_ok = True)

# 读images数据
for data_path in ['val.json', 'train.json']:

    data = json.load(open(data_path, 'r', encoding='utf-8'))
    _img_dir = os.path.join(img_dir, data_path.split('.')[0]).replace('\\', '/')
    _label_dir = os.path.join(label_dir, data_path.split('.')[0]).replace('\\', '/')
    os.makedirs(_img_dir, exist_ok = True)
    os.makedirs(_label_dir, exist_ok = True)
    idDatas = {}
    ids = []

    for _data in data['images']:

        file_name = _data['file_name']
        image_id = _data['id']
        w = _data['width']
        h = _data['height']

        _idData = {}
        _idData['width'] = w
        _idData['height'] = h
        _idData['file_name'] = file_name

        if 'annotations' in _data:
            an_data_new = []
            an_data = _data['annotations']

            for _an_data in an_data:
                if _an_data['id'] not in ids:
                    an_data_new.append(_an_data)

            _idData['annotations'] = an_data_new
        idDatas[image_id] = _idData

    for _data in data['annotations']:
        image_id = _data['image_id']
        if 'annotations' not in idDatas[image_id]:
            idDatas[image_id]['annotations'] = []
        if _data['id'] not in ids:
            idDatas[image_id]['annotations'].append(_data)

    _data_dir = os.path.join('./', data_path.split('.')[0])

    for k, idData in tqdm(idDatas.items()):
        img_name = idData['file_name']
        img_path = os.path.join(_data_dir, img_name).replace('\\', '/')
        to_img_path = os.path.join(_img_dir, img_name).replace('\\', '/')

        W = idData['width']
        H = idData['height']
        annotation = idData['annotations']

        shutil.copyfile(img_path, to_img_path)
        
        label_path = os.path.join(_label_dir, '{}.txt'.format(img_name.split('.')[0]))
        with open(label_path, 'w', encoding = 'utf-8') as f:
            for _annotation in annotation:
                x, y, w, h = _annotation['bbox']
                category_id = str(_annotation['category_id'] - 1)
                xc = str((x + w / 2) / W)
                yc = str((y + h / 2) / H)
                w = str(w / W)
                h = str(h / H)

                f.write('{} {} {} {} {}\n'.format(category_id, xc, yc, w, h))
