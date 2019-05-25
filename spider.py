import codecs
from lxml import etree
import time
import requests
import re
import csv
from PyQt5.QtCore import QThread,pyqtSignal

class CrawlThread(QThread):
    log_signal = pyqtSignal(str)
    def __init__(self,job):
        super(CrawlThread, self).__init__()

        self.headers = {
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',}
        self.job=job
        self.url =r"https://www.zhipin.com/c100010000/?query="+job+"&page="
        self.domain ="https://www.zhipin.com"
    def run(self):

            self.fp = open('img/test.csv', 'a', encoding='utf-8_sig', newline="")
            headers = ['name', 'salary', 'city', 'work_years', 'education', 'company', 'job_request', 'company_detail',
                   'company_size', 'company_caterogy', 'company_date', 'company_money', 'company_type',
                   'company_stauts']
            self.writer = csv.DictWriter(self.fp, headers)
            self.writer.writeheader()
            for i in range(1,11):
                new_url =self.url + str(i)
                response = requests.get(url=new_url,headers=self.headers)

                html = etree.HTML(response.text)
                links = html.xpath("//div[@class='info-primary']//h3[@class='name']/a/@href")
                if(len(links)==0):
                    self.log_signal.emit("不好意思，你输入的关键字有误，或者是你的信息已经爬完,也可能你的IP被封了")
                for link in links:
                    link = self.domain + link
                    self.parse_detail(link)

                    time.sleep(2)
                time.sleep(2)

    def parse_detail(self,link):
        response = requests.get(url=link, headers=self.headers)
        self.log_signal.emit(str(response))
        html = etree.HTML(response.text)
        #岗位名称
        name = html.xpath("//div[@class='name']/h1/text()")[0].strip()
        #薪水
        salary = html.xpath("//div[@class='name']/span[@class='badge']/text()")[0].strip()
        #城市
        city = html.xpath("//div[@class='info-primary']/p/text()")[0].split("：")[0]
        #经验要求
        exeperience = html.xpath("//div[@class='info-primary']/p/text()")[1].split("：")[0]
        #学历要求
        education = html.xpath("//div[@class='info-primary']/p/text()")[2].split("：")[0]
        #公司名称
        company = html.xpath("//div[@class='company-info']//a/@title")[0].strip()
        #岗位要求
        desc = re.split(r'\\n', ("".join(html.xpath("//div[@class='text']/text()")).strip()))[0]
        #公司是否需要融资
        #公司规模
        company_zong = html.xpath("//div[@class='sider-company']/p/text()")
        if len(company_zong)<3:
            company_detail = "不详"
            company_size =company_zong[1].strip()
        else:
            company_detail = company_zong[1].strip()
            company_size = company_zong[2].strip()

        #公司类别
        company_caterogy = html.xpath("//div[@class='sider-company']/p/a/text()")[0].strip()
        #公司注册时间
        company_date = html.xpath("//div[@class='level-list']/li[@class='res-time']/text()")
        if (len(company_date) == 0):
            company_date = "没有-注册"
        else:
            company_date = company_date[0]
        #公司注册资金
        company_all = html.xpath("//div[@class='level-list']/li/text()")
        if(len(company_all)==0):
            company_money ="不详"
            company_type = "不详"
            company_stauts = "不详"
        else:
            company_money = html.xpath("//div[@class='level-list']/li/text()")[1].strip()
            #公司详情
            company_type = html.xpath("//div[@class='level-list']/li/text()")[-2].strip()
            #公司状态
            company_stauts = html.xpath("//div[@class='level-list']/li/text()")[-1].strip()
        self.position = {
            'name':name,
            'salary':salary,
            'city':city,
            'work_years':exeperience,
            'education':education,
            'company':company,
            'job_request':desc,
            'company_detail':company_detail,
            'company_size':company_size,
            'company_caterogy':company_caterogy,
            'company_date':company_date,
            'company_money':company_money,
            'company_type':company_type,
            'company_stauts':company_stauts

        }
        self.log_signal.emit(str(self.position))
        self.writer.writerow(self.position)


