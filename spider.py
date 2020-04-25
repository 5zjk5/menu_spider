import requests
import csv
from lxml import etree
from fake_useragent import UserAgent


def create_csv():
    '''
    创建 foods.csv, soups.csv
    '''
    head = ['name','food','score','link']
    csvs = ['foods.csv','soups.csv']
    for c in csvs:
        with open(c,'w',encoding='gbk',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(head)


def get_html(url,kind):
    '''
    请求 html
    '''
    headers = {
        'User-Agent' : UserAgent().random,
        'Cookie' : 'bid=SUKKdKjF; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22171a785835191-0292964d820ab7-4313f6a-921600-171a78583520%22%2C%22%24device_id%22%3A%22171a785835191-0292964d820ab7-4313f6a-921600-171a78583520%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; __utmz=177678124.1587653477.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=e0150cd671284025:T=1587653477:S=ALNI_Mbm6h5yX4RCMFDKDV9SBCRwZXLwFg; Hm_lvt_ecd4feb5c351cc02583045a5813b5142=1587653477,1587700573; __utma=177678124.702716191.1587653477.1587653477.1587700573.2; __utmc=177678124; __utmb=177678124.44.10.1587700573; Hm_lpvt_ecd4feb5c351cc02583045a5813b5142=1587703641',
        'Host' : 'www.xiachufang.com',
        'Referer' : kind.split('?')[0]
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response
    else:
        return


def get_infos(response):
    '''
    提取数据
    '''
    infos = []
    html = etree.HTML(response.text)
    menus = html.xpath('//ul[@class="list"]/li')[:20]

    for menu in menus:
        name = menu.xpath('./div/div/p[1]/a/text()')[0].replace('\n','').replace(' ','')
        food = menu.xpath('./div/div/p[@class="ing ellipsis"]')[0]
        food = food.xpath('string(.)').replace('\n','').replace(' ','')
        score = menu.xpath('./div/div/p[3]/span[1]/text()')[0]
        link = menu.xpath('./div/div/p[1]/a/@href')[0]
        link = 'http://www.xiachufang.com' + link

        infos.append([name,food,score,link])

    return infos


def write_to_csv(infos,file):
    '''
    写入 csv
    '''
    with open(file,'a+',encoding='utf8',newline='') as f:
        writer = csv.writer(f)
        for info in infos:
            writer.writerow(info)


if __name__ == '__main__':
    count = 1
    create_csv()
    kind_urls = ['http://www.xiachufang.com/category/40076/',
                 'http://www.xiachufang.com/category/40077/',
                 'http://www.xiachufang.com/category/40078/',
                 'http://www.xiachufang.com/category/20130/']
    for kind in kind_urls:
        kind += '?page={}'
        urls = [kind.format(str(i)) for i in range(1,12)]
        for url in urls:
            response = get_html(url,kind)
            if response == None:
                continue
            infos = get_infos(response)

            # 判断是否为【汤羹】url，写入对应的 csv
            if '20130' not in url:
                file = 'foods.csv'
            else:
                file = 'soups.csv'
            write_to_csv(infos,file)

            print('已爬取 %d 页菜谱' % count)
            count += 1



