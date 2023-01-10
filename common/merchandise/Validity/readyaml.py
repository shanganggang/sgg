# @time :2022/12/28 17:26
# @author:EDY
# @file :readyaml.py
import yaml
import os


def dirname(filepath, filename):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), filename, filepath)


def readyaml(yumlurl):
    with open(dirname(yumlurl, '../../config/merchandise/Validity'), 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)  # yaml.load  将f.data的字符串类型转化为字典类型，Loader=yaml.FullLoader为默认标准用法
    return data
