#encoding: utf-8

import requests
import re
import json

def spider(sn, book_list=[]):
    '''analyze data from taobao'''
    url = 'https://s.taobao.com/search?q={0}'.format(sn)
    headers = {
        'user-agent':'537.36',
        'cookie':'isg=BFBQDmabO_xJyef64qYjEsRoI5iiGTRjM9NIpkoh5qt-hfEv8i3r8_P_XcVlTuw7; l=eBxW7y5rOrJEw48kBO5BPurza77TXIR08kPzaNbMiInca6OF9FgpFNQqxoI6Wdtf_tfA2etrB4JD3RHvyZ4N914Ki2trCyCodxJ6-; tfstk=c9uFBgq0yzDsBp4Y-yaPR-diO84daEgmyOP7xmphKdS6JwzYgsh4yD5JlIN5XgC..; uc1=pas=0&existShop=false&cookie21=UIHiLt3xThH8t7YQoFNq&cookie14=UoTV6hJ13oZ2VA%3D%3D&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D; JSESSIONID=BE412B082D3464204E8C19354A5C0CC3; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _m_h5_tk=a3eb0b835ff8ed2fa188a07971750ee4_1596944114115; _m_h5_tk_enc=6d125d8bd0fedc7716ef6d4a6e43ee51; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=91_1; thw=cn; enc=9QimX642bIwNLppux5TJxC%2Fr3QKGdyk56%2BYrjPwclphpmT3zmAcZRX4k4TIH0SKpYvikHdtvwpN0%2BhFtSw2hFg%3D%3D; _cc_=UtASsssmfA%3D%3D; _tb_token_=e5755659eb685; cookie2=1bbf714972351845268a4879cf574956; csg=c99a330e; dnk=%5Cu96EA%5Cu5B9D%5Cu7231%5Cu67E0%5Cu6AAC; existShop=MTU5Njc5MTAxMA%3D%3D; lgc=%5Cu96EA%5Cu5B9D%5Cu7231%5Cu67E0%5Cu6AAC; sgcookie=EtxdZbFO1CEDzXBGsNjBM; skt=8bdf70009cbceb66; t=292d535823fd365da4b80181e7a6b397; tracknick=%5Cu96EA%5Cu5B9D%5Cu7231%5Cu67E0%5Cu6AAC; uc3=lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dBxG2jhEDAqFvtm00%3D&id2=UNDULYsPz5jbUw%3D%3D&nk2=sqZitJm%2FBqdy5A%3D%3D; uc4=id4=0%40UgckFdMYDgRguJ3R3yjHR27%2BiJad&nk4=0%40sK62FdqGdSfkpMqabCcmy8urCLvv; _samesite_flag_=true; cna=ywa0F1B0bi4CAdpel8kfB/KZ; v=0'
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

        book_list.append({
            'title': title,
            'price': price,
            'link': link,
            'store': store
        })


if __name__ == '__main__':
    sn = '9787115428028'
    spider(sn)