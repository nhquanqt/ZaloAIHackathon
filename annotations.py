import json
import os
import cv2
import random as rd

DATASET_DIR = '/home/wan/ZaloAIHackathon/data/zai2019_hackaton_train/images/train'
ANNO_FILE = '/home/wan/ZaloAIHackathon/data/zai2019_hackaton_train/annotations/ninedash_keypoints_train.json'
OUT_FILE = '/home/wan/ZaloAIHackathon/data/dataset/dataset.txt'


def draw(image, bbox):
    x = bbox[0]
    y = bbox[1]
    b_w = bbox[2]
    b_h = bbox[3]

    dst = cv2.rectangle(image, (x, y), (x+b_w, y+b_h), (0,255,0), 10)
    # dst = cv2.rectangle(image, (x_center-b_h//2, y_center-b_w//2), (x_center+b_h//2, y_center+b_w//2), (0,255,0), 10)
    # cv2.imshow('Show', dst)
    # cv2.waitKey(0)
    return dst

def find(image_json, id):
    for image in image_json:
        if image['id'] == id:
            return image
    
    return None

if __name__ == "__main__":
    anno = json.load(open(ANNO_FILE))
    out_file = open(OUT_FILE, 'w')

    image_json = anno['images']
    gt_json = anno['annotations']

    # idx = 10
    # f_image = image_json[idx]['file_name']
    # image = cv2.imread(os.path.join(DATASET_DIR,f_image))
    # bbox = gt_json[idx]['bbox']
    # draw(image, bbox)


    image_num = len(image_json)
    print(len(image_json))
    print(len(gt_json))
    for gt in gt_json:
        idx = gt['image_id']
        # print idx
        image_j = find(image_json, idx)

        f_image = image_j['file_name']

        image_h = image_j['height']
        image_w = image_j['width']
        x_min = gt['bbox'][0]
        y_min = gt['bbox'][1]
        b_w = gt['bbox'][2]
        b_h = gt['bbox'][3]
        cv2.imwrite('./test/'+f_image, draw(cv2.imread(os.path.join(DATASET_DIR,f_image)), gt['bbox']))
        # x_max = min(x_min + b _w, image_w-1)
        x_max = x_min + b_w-1
        # if x_max >= image_w:
        #     # print 'Error'
        #     print 'W', f_image, x_max, image_w
        # y_max = min(y_min + b_h, image_h-1)
        y_max = y_min + b_h-1
        # if y_max >= image_h:
        #     # print 'Error'
        #     print 'H', f_image, y_max, image_h
        image = cv2.imread(os.path.join(DATASET_DIR,f_image))


        x_min = max(1, x_min)
        y_min = max(1, y_min)
        x_max = min(image_w-1, x_min)
        y_max = min(image_h-1, y_min)
        print image.shape, x_min, y_min, x_max, y_max, image_h, image_w
        out_file.write('{} {},{},{},{},0\n'.format(os.path.join(DATASET_DIR,f_image), x_min, y_min, x_max, y_max))
        # print('{} {}, {}, {}, {}, {} {}'.format(os.path.join(DATASET_DIR,f_image), x_min, y_min, x_max, y_max, image_h, image_w))