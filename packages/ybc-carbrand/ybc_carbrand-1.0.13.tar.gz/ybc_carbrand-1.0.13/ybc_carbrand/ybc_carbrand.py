import json
import os
from ybc_exception import *

_PATH = os.path.abspath(__file__)
_DATA_PATH = os.path.split(_PATH)[0]+'/data/carbrands.json'


def brands():
    """
    功能：获取所有汽车品牌。

    参数：无

    返回：所有汽车品牌
    """
    try:
        f = open(_DATA_PATH, encoding='utf-8')
        file_json = json.load(f)
        return file_json

    except Exception as e:
        raise InternalError(e, 'ybc_carbrand')


def main():
    print(brands())


if __name__ == '__main__':
    main()
