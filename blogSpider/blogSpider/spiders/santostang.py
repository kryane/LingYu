import scrapy
from bs4 import BeautifulSoup
from blogSpider.items import BlogspiderItem


class SantostangSpider(scrapy.Spider):
    name = 'santostang'
    allowed_domains = ['www.santostang.com']
    start_urls = ['http://www.santostang.com/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # first_title = soup.find('h1', class_='post-title').a.text.strip()
        # print('第一篇文章的标题是：', first_title)
        title_list = soup.find_all('h1', class_='post-title')
        for i in range(len(title_list)):
            # 将数据封装到BlogspiderItem对象，字典类型
            item = BlogspiderItem()
            title = title_list[i].a.text.strip()
            link = title_list[i].a['href']
            # print('第%s篇文章的标题是：%s' % (i + 1, title))
            # 生成字典
            item['title'] = title
            item['link'] = link
            # 获取相关文章链接，发送requests请求，并传递item参数
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        # 解析提取文章内容
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('div', class_='view-content').text.strip()
        content = content.replace('\n', '')
        item['content'] = content
        # 返回item，交给item pipeline
        yield item
