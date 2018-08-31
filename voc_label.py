import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

classes = ["clip","nut","loader","spacer","pond","slip touch","damaged","excavator","shockproof hammer","slip touch","damaged","excavator","shockproof hammer","insulator","smog","parachute","tower","floating on","houses","construction","background","crane","drilling machine","Drilling machine","roller","kentucky","underground film","dowel","bamboo","strapping","nut rusting","armour clamp","rust" ]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(path):
    filenames = os.listdir(path)
    fh_train = open("/workspace/train-guanggong.txt", "w")
    fh_test = open("/workspace/test-guanggong.txt", "w")

    fh1_train = open("./ImageSets/Main/train.txt", "w")
    fh1_test = open("./ImageSets/Main/test.txt", "w")
    count = 0;
    # print filenames
    for filename in filenames:
        count += 1
        if (count <= 5000):
            fh_train.write("/workspace/zengming_guanggong/orig_samples/data/VOC2007/JPEGImages/" + filename.split(".")[0] + ".jpeg" + '\n')
            fh1_train.write(filename.split(".")[0] + '\n')
        else:
            fh_test.write("/workspace/zengming_guanggong/orig_samples/data/VOC2007/JPEGImages/" + filename.split(".")[0] + ".jpeg" + '\n')
            fh1_test.write(filename.split(".")[0] + '\n')

        in_file = open(path + filename)
        # print in_file
        out_file = open("./labels/%s.txt"%filename.split(".")[0],"w")  # split the filename without suffix
        tree=ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        # print size
        w = int(size.find('width').text)
        # print w
        h = int(size.find('height').text)
        # print h
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text

            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            # print cls_id
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            # print bb
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            # print str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n'

        in_file.close()
        out_file.close()
    fh_train.close()
    fh_test.close()
    fh1_train.close()
    fh1_test.close()

if __name__ == "__main__":
    if not os.path.exists('./labels/'):
        os.makedirs('./labels/')
    convert_annotation("./Annotations/")
