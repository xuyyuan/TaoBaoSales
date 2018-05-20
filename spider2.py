import requests
import re
import json

keyword = input('请输入关键词：')
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

def get_one_page(page):
    url = 'https://s.taobao.com/search?q=' + keyword +  '&sort=sale-desc&s=' + str(page*44)
    res = requests.get(url, headers=headers)
    pattern = re.compile(r'.*?g_page_config = (.*?);\n', re.S)
    result = re.search(pattern, res.text)
    if result:
        data = result.group(1)
        # data = json.loads(data)  # 配合下面find_keys(data, lever)使用
        return data

def parse_one_page(data):
    data = json.loads(data)
    result = data['mods']['itemlist']['data']
    for each in result.get('auctions'):
        yield {
            'nid':each.get('nid'),
            'title':each.get('title'),
            'raw_title':each.get('raw_title'),
            'nick':each.get('nick'),
            'view_sales':each.get('view_sales')[:-3],
            'view_price':each.get('view_price'),
            'item_loc':each.get('item_loc')
        }

if __name__ == '__main__':
    total = 0
    for page in range(3):  # 这里只设定为三页
        data = get_one_page(page)
        for each in parse_one_page(data):
            if '小甲鱼' in each.get('title'):   # 有可能再each.get('raw_title')中，可以加上一个判断
                print(int(each.get('view_sales')))
                total += int(each.get('view_sales'))
    print(total)

"""
#用来查找字典中的键和值的
def get_space_end(lever):
    return '  '*lever + '-'

def get_space_expand(lever):
    return '  '*lever + '+'

def find_keys(data,lever):
    #data = json.loads(data)    # 这里加上这一句就会报错，因为存在‘递归函数’；
    for each in data.keys():
        if type(data.get(each)) is not dict:
            print(get_space_end(lever), each)
        else:
            print(get_space_expand(lever), each)
            next_lever = lever + 1    # 注意一下这里用 lever += 1 是不行的！！！
            find_keys(data.get(each), next_lever) # 递归
"""

