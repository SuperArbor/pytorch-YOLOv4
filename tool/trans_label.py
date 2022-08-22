import os, sys, json, re
from pprint import pprint

dir = os.path.dirname(os.path.abspath(__file__))
path_config = os.path.join(dir, "trans_label.config.json")

with open(path_config, mode='r', encoding='utf-8') as f:
    config = json.load(f)
    path_json = config['path_json']
    path_train = config['path_train']
    path_val = config['path_val']
    path_cls = config['path_cls']
    ratio_train = config['ratio_train']
    class_map = {}
    dir_map = config['dir_map']

    outputs = []
    with open(path_json, mode='r', encoding='utf-8') as fj:
        # with open(path_train, mode='w', encoding='utf-8') as ft, open(path_val, mode='w', encoding='utf-8') as fv:
            entries = json.load(fj)
            for entry in entries:
                image_path = entry['data']['image']
                for key in dir_map.keys():
                    if re.match(key, image_path):
                        image_path = re.sub(key, dir_map[key], image_path)
                output = []
                for annotation in entry['annotations']:
                    for result in annotation['result']:
                        empty = False
                        value = result['value']
                        x1, y1 = value['x'], value['y']
                        x2, y2 = x1 + value['width'], y1 + value['height']
                        cls = value['rectanglelabels'][0]
                        if cls in class_map.keys():
                            id = class_map[cls]
                        else:
                            id = len(class_map)
                            class_map[cls] = id
                        output.append(','.join([str(i) for i in [x1, y1, x2, y2, id]]))
                if output:
                    output.insert(0, image_path)
                    # ft.write(' '.join(output) + '\n')
                    outputs.append(output)
            
    num_train = int(ratio_train * len(outputs))
    num_val = len(outputs) - num_train

    with open(path_train, mode='w', encoding='utf-8') as f:
        for i in range(num_train):
            f.write(' '.join(outputs[i]) + '\n')

    with open(path_val, mode='w', encoding='utf-8') as f:
        for i in range(num_val):
            f.write(' '.join(outputs[num_train + i]) + '\n')

    with open(path_cls, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(class_map))
