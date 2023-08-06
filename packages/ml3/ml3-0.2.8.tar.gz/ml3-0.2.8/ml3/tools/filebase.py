"""

"""

import json
import csv
import os
import logging


def load_json_file(path):
    """
    加载json文件
    :param path: json文件路径
    :return: json文件的内容，如果加载失败，则返回None
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
            return content
    except Exception as e:
        print (e)
        return None


def dump_json_file(json_content, path, **kwargs):
    """
    写入到json文件
    :param file_list: json文件内容
    :param path: 需要写入的文件路径
    :return: 如果写入成功，则返回True，否则返回False
    """
    dir_name = os.path.dirname(path)
    if dir_name == "." or dir_name == "":
        pass
    elif not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if path[-5:] != '.json':
        print ("必须导出成json文件.")
        return False
    #当json中有中文字符串时，需要在open时加上encoding=‘utf-8'，dump时加上ensure_ascii=False，
    try:
        with open(path, "w", encoding="utf-8", newline='') as f:
            if 'indent' in kwargs:
                json.dump(json_content, f, indent=int(kwargs['indent']), ensure_ascii=False)
            else:
                json.dump(json_content, f, ensure_ascii=False)
            return True
    except Exception as e:
        print (e)
        return True


def load_csv_file(path):
    """
    加载csv文件
    :param path: csv文件路径
    :return: csv文件的内容，如果加载失败，则返回None
    """
    file_list = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            all_line = csv.reader(f)
            for one_line in all_line:
                file_list.append(one_line)
        return file_list
    except Exception as e:
        print (e)
        return None


def dump_csv_file(file_list, path):
    """
    写入到csv文件
    :param file_list:csv文件列表
    :param path: 需要写入的文件路径
    :return:如果写入成功，则返回True，否则返回False
    """
    dir_name = os.path.dirname(path)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if path[-4:] != '.csv':
        print ("[Errno *] 传入的路径不是一个csv文件")
        return False
    # file_name = os.path.split(path)[-1]
    # print (file_name)
    try:
        with open(path, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(file_list)
            return True
    except Exception as e:
        print (e)
        return None



