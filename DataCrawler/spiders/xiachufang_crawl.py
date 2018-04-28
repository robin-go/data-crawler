# -*- coding: utf-8 -*-
from w3lib.html import remove_tags

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from DataCrawler.items import RecipeItem


class XiachufangCrawlSpider(CrawlSpider):
    name = 'xiachufang_crawl'
    allowed_domains = ['xiachufang.com']
    start_urls = ['http://www.xiachufang.com/']

    rules = (
        Rule(LinkExtractor(allow=r'category/\d+'), follow=True),
        Rule(LinkExtractor(allow=r'category/\d+/?page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'recipe/\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        """
        解析详情页,获取食谱,并输出到pipeline
        """

        item = RecipeItem()

        # 菜名
        title = response.xpath("//h1[@class='page-title']/text()").extract_first('').strip()

        # 用料
        material_selectors = response.xpath("//div[@class='ings']//tr")

        material_list = []
        for selector in material_selectors:
            # 材料
            s1 = selector.xpath("./td[1]").extract_first('')
            s1 = remove_tags(s1).strip()
            # 用量
            s2 = selector.xpath("./td[2]/text()").extract_first('').strip()

            s = s1 + "：" + s2 if s2 else s1
            material_list.append(s)

        materials = '\n'.join(material_list)

        # 做法
        step_list = response.xpath("//div[@class='steps']/ol/li/p").extract()

        step_list = [str(index) + '：' + remove_tags(step) for index, step in enumerate(step_list, 1)]
        steps = '\n'.join(step_list)

        # 评分
        rank = response.xpath("//span[@itemprop='ratingValue']/text()").extract_first('0')

        # url
        url = response.url

        item['title'] = title
        item['materials'] = materials
        item['steps'] = steps
        item['rank'] = rank
        item['url'] = url

        return item
