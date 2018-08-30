#coding:utf-8
import glob
import xml.etree.ElementTree as ET
from kmeans import kmeans, avg_iou
import numpy as np

def load_dataset(path, dirlist):
    dataset = []
    for dirname in dirlist:
        print(dirname)
        for xml_file in glob.glob("{}/*.xml".format(path + dirname)):
            print("--------------------")
            tree = ET.parse(xml_file)

            height = int(tree.findtext("./size/height"))
            width = int(tree.findtext("./size/width"))


            for obj in tree.iter("object"):
                xmin = int(obj.findtext("bndbox/xmin")) / width
                ymin = int(obj.findtext("bndbox/ymin")) / height
                xmax = int(obj.findtext("bndbox/xmax")) / width
                ymax = int(obj.findtext("bndbox/ymax")) / height
                print("------------------------------------------")
                dataset.append([xmax - xmin, ymax - ymin])

    return np.array(dataset)

if __name__ == "__main__":
        data = load_dataset("./", ['0', '1'])
        print(data.shape)
        print(data)
        print("Start Cluster:")
        out = kmeans(data, k=5)
        print("5 Clusters is: ")
        print(out)
        
        print("Start Cluster:")
        out = kmeans(data, k=7)
        print("7 Clusters is: ")
        print(out)
        
        print("Start CLuster:")
        out = kmeans(data, k=9)
        print("9 Clusters is: ")
        print(out)

