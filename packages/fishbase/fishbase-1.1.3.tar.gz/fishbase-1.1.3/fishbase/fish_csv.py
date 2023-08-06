# coding=utf-8
import csv
from io import open


# 将指定的 csv 文件转换为 list 返回
# 输入：
# csv_filename: csv 文件的长文件名
# deli: csv 文件分隔符，默认为逗号
# del_blank_row: 是否要删除空行，默认为删除
# 输出：转换后的 list
# ---
# 2018.2.1 edit by David Yi, #11002
# 2018.2.6 edit by David Yi, #11009， 增加过滤空行功能
# v1.0.16 edit by Hu Jun #94
def csv_file_to_list(csv_filename, deli=',', del_blank_row=True, encoding=None):

    """
    将指定的 csv 文件转换为 list 返回；

    :param:
        * csv_filename: (string) csv 文件的长文件名
        * deli: (string) csv 文件分隔符，默认为逗号
        * del_blank_row: (string) 是否要删除空行，默认为删除
        * encode: (string) 文件编码
    :return:
        * csv_list: (list) 转换后的 list

    举例如下::

        from fishbase.fish_file import *
        from fishbase.fish_csv import *

        def test_csv():
            csv_filename = get_abs_filename_with_sub_path('csv', 'test_csv.csv')[1]
            print(csv_filename)
            csv_list = csv_file_to_list(csv_filename)
            print(csv_list)


        if __name__ == '__main__':
            test_csv()

    """
    with open(csv_filename, encoding=encoding) as csv_file:
        csv_list = list(csv.reader(csv_file, delimiter=deli))

    # 如果设置为要删除空行
    if del_blank_row:
        csv_list = [s for s in csv_list if len(s) != 0]

    return csv_list
