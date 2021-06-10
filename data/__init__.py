# -*- coding: utf-8 -*-
# Author    ：Yang Ming
# Create at ：2021/6/10
# tool      ：PyCharm

import os
import pathlib

root = pathlib.Path(__file__).absolute().parents[0]

data_path = os.path.join(root,'__token__.json')
google_sheet_key_path = os.path.join(root,'apartments-crawler-a62ef21f06e2.json')

if __name__ == '__main__':
    print(data_path)