import cv2
import numpy as np
import os
import shutil
import time
import argparse


class HashTracker:
    def __init__(self, path):
        # 初始化图像
        self.img = cv2.imread(path)
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def cal_hash_code(self, cur_gray):
        s_img = cv2.resize(cur_gray, dsize=(8, 8))
        img_mean = cv2.mean(s_img)
        return s_img > img_mean[0]

    def cal_phash_code(self, cur_gray):
        # 缩小至32*32
        m_img = cv2.resize(cur_gray, dsize=(32, 32))
        # 浮点型用于计算
        m_img = np.float32(m_img)
        # 离散余弦变换，得到dct系数矩阵
        img_dct = cv2.dct(m_img)
        img_mean = cv2.mean(img_dct[0:8, 0:8])
        # 返回一个8*8bool矩阵
        return img_dct[0:8, 0:8] > img_mean[0]

    def cal_dhash_code(self):
        cur_gray = self.gray
        # dsize=(w-idth, height)
        m_img = cv2.resize(cur_gray, dsize=(9, 8))
        m_img = np.int8(m_img)
        # 得到8*8差值矩阵
        m_img_diff = m_img[:, :-1] - m_img[:, 1:]
        return np.piecewise(m_img_diff, [m_img_diff > 0, m_img_diff <= 0], [1, 0])

    def cal_hamming_distance(self, model_hash_code, search_hash_code):
        # 返回不相同的个数
        diff = np.uint8(model_hash_code - search_hash_code)
        return cv2.countNonZero(diff)


def search(path, name):
    for root, dirs, files in os.walk(path):  # path 为根目录
        if name in dirs or name in files:
            return 0
    return -1


def hash2txt(url_pic, url_txt):
    print('to txt ing...')
    for path in os.listdir(url_pic):
        if path[-1] == 'g':
            h = HashTracker(url_pic + '/' + path)
            matrix = h.cal_dhash_code()
            array = matrix.reshape([-1])
            name = url_txt + '/' + path + '.txt'
            np.savetxt(name, array, fmt="%d")
    print('txt all')
    return 0


def find1(url_txt, url_pic, url_move_txt, url_move_pic):
    lens = len(os.listdir(url_txt))
    repeat_item = []
    repeat_txt_list = []
    repeat_pic_list = []
    dlist = os.listdir(url_txt)
    dlist_pic = os.listdir(url_pic)
    time_now = time.strftime("%m-%d", time.localtime())
    if search(os.path.abspath('.'), 'out_folder') == -1:
        os.mkdir('out_folder')
    if search('out_folder', time_now) == -1:
        os.mkdir('out_folder/' + time_now)
    for i in range(lens - 1):
        if i not in repeat_item:
            path = url_txt + '/' + dlist[i]
            f = open(path)
            str = f.read()
            f.close()
            list = str.split('\n')
            list = list[:-1]
            new_list = [int(p) for p in list]
            arr = np.array(new_list)
            matrix_1 = arr.reshape([8, 8])
            j = i + 1
            for j in range(j, lens):
                if j not in repeat_item:
                    path = url_txt + '/' + dlist[j]
                    f = open(path)
                    str = f.read()
                    f.close()
                    list = str.split('\n')
                    list = list[:-1]
                    new_list = [int(p) for p in list]
                    arr = np.array(new_list)
                    matrix_2 = arr.reshape([8, 8])
                    diff = matrix_1 - matrix_2
                    diff_int = (np.sum(np.abs(diff)))
                    if diff_int <= 4:
                        print('repeated items- diff_int:{}   jpg1:{}   jpg2:{}'.format(diff_int, os.listdir(url_pic)[i], os.listdir(url_pic)[j]))
                        repeat_item.append(j)
                        repeat_txt_list.append(url_txt + '/' + dlist[j])
                        repeat_pic_list.append(url_pic + '/' + dlist_pic[j])

    for re in range(len(repeat_txt_list)):
        shutil.move(repeat_txt_list[re], url_move_txt)
        shutil.move(repeat_pic_list[re], url_move_pic)

    lens = len(os.listdir(url_pic))
    dlist_pic = os.listdir(url_pic)
    for n in range(lens):
        shutil.move(url_pic + '/' + dlist_pic[n], 'out_folder' + '/' + time_now)


def main(dataset):
    if search(os.path.abspath('.'), 'txt') == -1:
        os.mkdir('txt')
    url_txt = 'txt'  # 输出array文本地址
    hash2txt(dataset, url_txt)
    if search(os.path.abspath('.'), 'move_txt') == -1:
        os.mkdir('move_txt')
    url_move_txt = 'move_txt'  # 保存重复array文本文件夹地址
    if search(os.path.abspath('.'), 'move_pic') == -1:
        os.mkdir('move_pic')
    url_move_pic = 'move_pic'  # 保存重复图片文件夹地址
    find1(url_txt, dataset, url_move_txt, url_move_pic)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", help="Path to original image dataset folder", default='G:/Duplicate Photo Finder/base')
    args = parser.parse_args()
    main(args.dataset)
