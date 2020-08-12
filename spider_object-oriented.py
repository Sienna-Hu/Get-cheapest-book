#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from lxml import html
import requests
import re
import json

class BookEntity():
    '''书本的基本信息'''
    def __init__(self, title, price, link, store):
        self.title = title
        self.price = price
        self.link = link
        self.store = store

    def __str__(self):
        return '名称：{self.title}；价格：{self.price}；购买链接：{self.link}；店铺：{self.store}'.format(self=self)

class MySpider(object):

    def __init__(self, sn):
        self.sn = sn
        # 存储所有的书的信息
        self.book_list = []

    def dangdang(self):
        '''爬取当当网的数据'''
        url = 'http://search.dangdang.com/?key={sn}&act=input'.format(sn=self.sn)
        # 获取html内容
        html_data = requests.get(url).text
        html_data.encode(encoding='utf-8')

        # xpath对象
        selector = html.fromstring(html_data)

        # 找到书本列表
        ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')
        print(len(ul_list))
        for li in ul_list:
            # 标题
            title = li.xpath('a/@title')
            print(title[0])
            # 购买链接
            link = li.xpath('a/@href')
            print(link[0])

            # 价格
            price = li.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')
            print(price[0].replace('¥',''))

            # 出版社
            store = li.xpath('p[@class="search_shangjia"]/a/text()')
            print('当当自营' if store == [] else store[0])

            book = BookEntity(
                title=title[0],
                price=price[0].replace('¥',''),
                link=link[0],
                store='当当自营' if store == [] else store[0]
            )
            self.book_list.append(book)

            print('-------------------------------------')

    def jd(self):
        '''爬取京东网的数据'''
        url = 'https://search.jd.com/Search?keyword={0}'.format(self.sn)
        # 获取HTML文档
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'

        html_doc = resp.text

        # 获取xpath对象
        selector = html.fromstring(html_doc)

        # 找到列表的集合
        ul_list = selector.xpath('//div[@id="J_goodsList"]/ul/li')
        print(len(ul_list))

        # 解析对应的内容，标题/价格/链接
        for li in ul_list:
            # title
            title = li.xpath('div/div[@class="p-name"]/a/@title')
            print(title[0])
            # link
            link = li.xpath('div/div[@class="p-name"]/a/@href')
            print(link[0])
            # price
            price = li.xpath('div/div[@class="p-price"]/strong/i/text()')
            print(price[0])
            # store
            store = li.xpath('div//a[@class="curr-shop hd-shopname"]/@title')
            print(store[0])

            book = BookEntity(
                title=title[0],
                price=price[0].replace('¥', ''),
                link=link[0],
                store='京东自营' if store == [] else store[0]
            )
            self.book_list.append(book)

    def taobao(self):
        '''爬取淘宝网的数据'''
        url = 'https://s.taobao.com/search?q={0}'.format(self.sn)
        headers = {
            'user-agent': '537.36',
            'cookie': 'isg=BFBQDmabO_xJyef64qYjEsRoI5iiGTRjM9NIpkoh5qt-hfEv8i3r8_P_XcVlTuw7; l=eBxW7y5rOrJEw48kBO5BPurza77TXIR08kPzaNbMiInca6OF9FgpFNQqxoI6Wdtf_tfA2etrB4JD3RHvyZ4N914Ki2trCyCodxJ6-; tfstk=c9uFBgq0yzDsBp4Y-yaPR-diO84daEgmyOP7xmphKdS6JwzYgsh4yD5JlIN5XgC..; uc1=pas=0&existShop=false&cookie21=UIHiLt3xThH8t7YQoFNq&cookie14=UoTV6hJ13oZ2VA%3D%3D&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D; JSESSIONID=BE412B082D3464204E8C19354A5C0CC3; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _m_h5_tk=a3eb0b835ff8ed2fa188a07971750ee4_1596944114115; _m_h5_tk_enc=6d125d8bd0fedc7716ef6d4a6e43ee51; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=91_1; thw=cn; enc=9QimX642bIwNLppux5TJxC%2Fr3QKGdyk56%2BYrjPwclphpmT3zmAcZRX4k4TIH0SKpYvikHdtvwpN0%2BhFtSw2hFg%3D%3D; _cc_=UtASsssmfA%3D%3D; _tb_token_=e5755659eb685; cookie2=1bbf714972351845268a4879cf574956; csg=c99a330e; dnk=%5Cu96EA%5Cu5B9D%5Cu7231%5Cu67E0%5Cu6AAC; existShop=MTU5Njc5MTAxMA%3D%3D; lgc=%5Cu96EA%5Cu5B9D%5Cu7231%5Cu67E0%5Cu6AAC; sgcookie=EtxdZbFO1CEDzXBGsNjBM; skt=8bdf70009cbceb66; t=292d535823fd365da4b80181e7a6b397; tracknick=%5Cu96EA%5Cu5B9D%5Cu7231%5Cu67E0%5Cu6AAC; uc3=lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dBxG2jhEDAqFvtm00%3D&id2=UNDULYsPz5jbUw%3D%3D&nk2=sqZitJm%2FBqdy5A%3D%3D; uc4=id4=0%40UgckFdMYDgRguJ3R3yjHR27%2BiJad&nk4=0%40sK62FdqGdSfkpMqabCcmy8urCLvv; _samesite_flag_=true; cna=ywa0F1B0bi4CAdpel8kfB/KZ; v=0'
        }

        # 获取html内容
        text = requests.get(url, headers=headers).text
        text.encode(encoding='utf-8')

        p = re.compile(r'g_page_config = (\{.+\});\s*', re.M)
        rest = p.search(text)
        if rest:
            print(rest.group(1))
            data = json.loads(rest.group(1))
            bk_list = data['mods']['itemlist']['data']['auctions']

            print (len(bk_list))
            for bk in bk_list:
                # 标题
                title = bk["raw_title"]
                print(title)
                # 价格
                price = bk["view_price"]
                print(price)
                # 购买链接
                link = bk["detail_url"]
                print(link)
                # 商家
                store = bk["nick"]
                print(store)

            book = BookEntity(
                title=title[0],
                price=price[0].replace('¥', ''),
                link=link[0],
                store='淘宝自营' if store == [] else store[0]
            )
            self.book_list.append(book)

    def spider(self):
        self.dangdang()
        self.jd()
        self.taobao()
        '''得到排序后的数据'''
        book_list = sorted(self.book_list, key=lambda item: float(item.price), reverse=True)
        for book in book_list:
            print(book)

if __name__ == '__main__':
     client = MySpider('9787115428028')
     client.spider()
