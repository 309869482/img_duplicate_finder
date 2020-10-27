import argparse
import numpy as np
import os
import shutil
import time
from base_pictures import search, hash2txt


def find1(url_txt, url_pic):
    lens = len(os.listdir(url_txt))
    repeat_item = []
    repeat_txt_list = []
    repeat_pic_list = []
    dlist = os.listdir(url_txt)
    dlist_pic = os.listdir(url_pic)
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
                        print('self——repeated items- diff_int:{}   jpg1:{}   jpg2:{}'.format(diff_int, dlist_pic[i], dlist_pic[j]))
                        repeat_item.append(j)
                        repeat_txt_list.append(url_txt + '\\' + dlist[j])
                        repeat_pic_list.append(url_pic + '\\' + dlist_pic[j])

    for re in range(len(repeat_txt_list)):
        os.remove(repeat_txt_list[re])
        os.remove(repeat_pic_list[re])


def find2(url_txt, url_txt_new, url_pic_new, url_move_txt, url_move_pic, url_txt_data):
    lens = len(os.listdir(url_txt))
    lens_new = len(os.listdir(url_txt_new))
    repeat_txt_list = []
    repeat_pic_list = []
    dlist_txt = os.listdir(url_txt)
    dlist_txt_new = os.listdir(url_txt_new)
    dlist_pic_new = os.listdir(url_pic_new)
    dlist_move_txt = os.listdir(url_move_txt)
    time_now = time.strftime("%m-%d", time.localtime())
    if search('out_folder', time_now) == -1:
        os.mkdir('out_folder/' + time_now)
    for i in range(lens_new):
        path = url_txt_new + '/' + dlist_txt_new[i]
        f = open(path)
        str = f.read()
        f.close()
        list = str.split('\n')
        list = list[:-1]
        new_list = [int(p) for p in list]
        arr = np.array(new_list)
        matrix_1 = arr.reshape([8, 8])

        for root, dirs, files in os.walk(url_txt):
            for name in files:
                path = os.path.join(root, name)
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
                    print('repeated items- diff_int:{}   jpg1:{}   jpg2:{}'.format(diff_int, name[:-4],
                                                                                   dlist_pic_new[i]))
                    repeat_txt_list.append(url_txt_new + '/' + dlist_txt_new[i])
                    repeat_pic_list.append(url_pic_new + '/' + dlist_pic_new[i])

    for re in range(lens_new):
        path_txt = url_txt_new + '/' + dlist_txt_new[re]
        path_pic = url_pic_new + '/' + dlist_pic_new[re]
        if path_txt not in repeat_txt_list:
            if dlist_txt_new[re] not in dlist_txt:
                shutil.copy(path_txt, url_txt_data)
                shutil.move(path_txt, url_txt)
                shutil.move(path_pic, 'out_folder' + '/' + time_now)
            else:
                os.remove(path_txt)
                os.remove(path_pic)
        else:
            if dlist_txt_new[re] not in dlist_move_txt:
                shutil.move(path_txt, url_move_txt)
                shutil.move(path_pic, url_move_pic)
            else:
                os.remove(path_txt)
                os.remove(path_pic)


def main(new_dataset):
    time_now = time.strftime("%m-%d", time.localtime())
    url_txt = 'txt'  # base 输出array文本地址
    if search(os.path.abspath('.'), 'txt_new') == -1:
        os.mkdir('txt_new')
    url_txt_new = 'txt_new'  # 保存新加图片array文本文件夹地址
    if search(os.path.abspath('.'), 'move_txt') == -1:
        os.mkdir('move_txt')
    url_move_txt = "move_txt"  # 保存重复array文本文件夹地址
    if search(os.path.abspath('.'), 'move_pic') == -1:
        os.mkdir('move_pic')
    url_move_pic = "move_pic"  # 保存重复图片文件夹地址
    if search(os.path.abspath('.'), 'txt_data') == -1:
        os.mkdir('txt_data')
    if search('txt_data', time_now) == -1:
        os.mkdir('txt_data/' + time_now)
    url_txt_data = 'txt_data' + '/' + time_now
    hash2txt(new_dataset, url_txt_new)
    find1(url_txt_new, new_dataset)
    find2(url_txt, url_txt_new, new_dataset, url_move_txt, url_move_pic, url_txt_data)
    # os.remove(url_txt_new)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", help="Path to new image dataset folder", default='G:/Duplicate Photo Finder/new')
    args = parser.parse_args()
    main(args.dataset)
