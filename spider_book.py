#encoding: utf-8

import json

from spider_dangdang import spider as dangdang
from spider_jd import spider as jd
from spider_taobao import spider as taobao

def main(sn, book_list):
    '''图书比价工具整合'''
    book_list =[]
    # 当当网的图书数据
    print('当当网数据爬取完成')
    dangdang(sn, book_list)

    # 京东的图书数据
    print('京东数据爬取完成')
    jd(sn, book_list)


    # 淘宝的图书数据
    print('淘宝数据爬取完成')
    taobao(sn, book_list)

    # 打印所有数据列表
    for book in book_list:
        print json.dumps(book, encoding="UTF-8", ensure_ascii=False)


    print('------------------------------------------------开始排序------------------------------------------------')


    # 排序书的数据
    book_list = sorted(book_list, key=lambda item:float(item['price']), reverse=False )
    for book in book_list:
        print json.dumps(book, encoding='utf-8', ensure_ascii=False)

if __name__ == '__main__':
    sn = input("请输入ISBN：")
    main(sn, book_list=[])