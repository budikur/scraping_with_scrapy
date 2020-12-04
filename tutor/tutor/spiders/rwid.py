from typing import List
import scrapy
from cssselect import Selector

class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['localhost']
    start_urls = ['http://localhost:5000/']

    def parse(self, response):
        # yield {"title": response.css("title::text").get()}
        # pass
        data = {
            "username": "user",
            "password": "user12345"
        }
        return scrapy.FormRequest(
            url="http://localhost:5000/login",
            formdata=data,
            callback=self.after_login
        )

    def after_login(self, response):
        """
        2 task di sini:
        1. ambil semua data barang yg ada di halaman hasil -> akan menuju detail (parsing detail)
        2. ambil semua link next -> akan balik ke self.after_login

        :param response:
        :return:
        """
        # get detail products
        detail_products: List[Selector] = response.css(".card .card-title a")
        for detail in detail_products:
            href = detail.attrib.get("href")
            yield response.follow(href, callback=self.parse_detail)

        paginations: List[Selector] = response.css(".pagination a.page-link")
        for pagination in paginations:
            href = pagination.attrib.get("href")
            yield response.follow(href, callback=self.after_login)

        # yield {"title": response.css("title::text").get()}
        # pass

    def parse_detail(self, response):
        # yield {"title": response.css("title::text").get()}
        image = response.css(".card-img-top").attrib.get("src")
        title = response.css(".card-title::text").get()
        stock = response.css(".card-stock::text").get()
        description = response.css(".card-text::text").get()

        return {
            "image": image,
            "title": title,
            "stock": stock,
            "desc": description
        }
