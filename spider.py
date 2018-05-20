import requests
import re
import json

def open_url(keyword, page):
	url = 'https://s.taobao.com/search'
	params = {'q':keyword, 'sort':'sale-desc', 's':str((page-1)*44)}
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
	res = requests.get(url, params=params, headers=headers)
    #比较之前项目，params = {'q': keyword, 'sort': 'sale-desc', 's': str((page - 1) * 44)}与我们的urlencode
	return res

def get_items(res):
	g_page_config = re.search(r'g_page_config = (.*?);\n', res.text).group(1)
	g_page_config_json = json.loads(g_page_config)
	page_items = g_page_config_json['mods']['itemlist']['data']['auctions']
	result = []
	for each_item in page_items:
		dict1 = dict()
		dict1 = dict1.fromkeys(('nid', 'title', 'detail_url', 'view_sales', 'nick'))
		dict1['nid'] = each_item['nid']
		dict1['title'] = each_item['title']
		dict1['detail_url'] = each_item['detail_url']
		dict1['view_sales'] = each_item['view_sales']
		dict1['nick'] = each_item['nick']
		result.append(dict1)
	return result

def count_sales(items):
	count = 0
	for each in items:
		if '小甲鱼' in each['title']:
			count += int(re.search(r'\d+', each['view_sales']).group())
	return count

def main():
	pages = 3
	total = 0
	keyword = input('请输入关键词：')
	for each in range(pages):
		res = open_url(keyword, each+1)
		items = get_items(res)
		total += count_sales(items)
	print('销量是：', total)

if __name__ == '__main__':
	main()




'''
# 用来查找json格式数据中的键和值的
def get_space_end(lever):
    return '  '*lever + '-'

def get_space_expand(lever):
    return '  '*lever + '+'

def find_keys(targets, lever):
    # keys = iter(targets)
    for each in targets:  # for each in keys:
        if type(targets[each]) is not dict:
            print(get_space_end(lever), each)
        else:
            print(get_space_expand(lever), each)
            next_lever = lever + 1
            find_keys(targets[each], next_lever)
'''
