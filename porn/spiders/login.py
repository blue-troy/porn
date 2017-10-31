import logging

import scrapy
from PIL import Image
from scrapy import Request

from porn.items import PornMovieItem


class login(scrapy.Spider):
    name = "login"
    logging_try_time = 0

    # 1 登陆
    # 1.1。先进入登陆页面
    def start_requests(self):
        url = 'http://91.91p09.space/login.php'
        yield Request(url)

    def parse(self, response):
        logging.info("process 获取验证码")
        url = 'http://91.91p09.space/captcha.php'
        yield Request(url, callback=self.parse_captcha)

    def parse_captcha(self, response):
        # 1.2 处理验证码
        logging.info("处理验证码 process parse_captcha")
        with open('captcha.png', 'wb') as f:
            f.write(response.body)
            f.close()
        # 1.3 输入验证码
        logging.info("输入验证码")
        captcha_img = Image.open('captcha.png')
        captcha_img.show()
        captcha_img.close()
        captcha = input("input the captcha with quotation mark\n>")
        logging.info("get input captcha = " + captcha)
        # 1.4。登陆请求
        return [scrapy.FormRequest("http://91.91p09.space/login.php",
                                   formdata={'user': 'your-user', 'password': 'your-passwd', 'captcha_input': captcha},
                                   callback=self.after_login)]

    # 2 登陆情况分发
    def after_login(self, response):
        if response.xpath('//*[@id="usermenu"]/div[1]/h4/text()').extract_first() == '我的状态':
            print('login success')
            return self.get_porn_start_requests()
        else:
            logging.warning('login error')
            self.logging_try_time = self.logging_try_time + 1
            if self.logging_try_time >= 2:
                logging.warning('please try a moment later')
            else:
                return self.start_requests()

    # 3 进入要爬的视频列表

    def get_porn_start_requests(self):
        url = 'http://91.91p09.space/v.php?category=top&viewtype=basic'
        yield Request(url, callback=self.parse_porn_list)

    # 4 获取视频页列表
    def parse_porn_list(self, response):
        movies = response.xpath('//div[@id="videobox"]/table//div[@class="listchannel"]')
        for movie in movies:
            movie_page = movie.xpath('.//a[@target="blank"]/@href').extract()[0]
            yield scrapy.Request(movie_page, self.parse_porn_movie)

    # 5 获取视频地址

    def parse_porn_movie(self, response):
        logging.info('.........................parse_porn_movie......................')
        movies = PornMovieItem()
        movies['file_urls'] = response.xpath('//source/@src').extract()
        movies['file_name'] = response.xpath('//div[@id="viewvideo-title"]/text()').extract()
        movies['files'] = response.xpath('//div[@id="viewvideo-title"]/text()').extract()
        yield movies
