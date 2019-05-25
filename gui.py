from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QMainWindow, QAction, QMenu, QTextBrowser, QFileDialog, \
    QGraphicsScene
from PyQt5.QtGui import QIcon, QImage, QPixmap
from spider import CrawlThread
import analysis
import os,stat
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
class Ico(QMainWindow):

   def __init__(self):
       super().__init__()
       self.initUI()

   def initUI(self):
       self.statusBar().showMessage('欢迎使用')

       self.setGeometry(300, 300,1000,600)
       self.setFixedSize(1000,600)

       self.setWindowTitle('Nano的毕设')
       self.setWindowIcon(QIcon('img/1.png'))

       self.text = QLineEdit('请输入你要爬取的职业或公司', self)
       self.text.selectAll()
       self.text.setFocus()
       self.text.setGeometry(100, 60, 250, 40)

       self.start_btn = QPushButton('爬取', self)
       self.start_btn.setGeometry(400, 60, 120, 40)
       self.start_btn.setToolTip('<b>点击这里爬取</b>')
       self.start_btn.clicked.connect(self.start_spider)

       self.stop_btn = QPushButton('停止', self)
       self.stop_btn.setGeometry(600, 60, 120, 40)
       self.stop_btn.setToolTip('<b>点击这里停止</b>')
       self.stop_btn.clicked.connect(self.stop_spider)
       self.stop_btn.setEnabled(False)

       self.analysis_btn = QPushButton('分析', self)
       self.analysis_btn.setGeometry(780, 60, 120, 40)
       self.analysis_btn.setToolTip('<b>点击这里分析</b>')
       self.analysis_btn.clicked.connect(self.analysis)
       self.analysis_btn.setEnabled(False)


       #菜单栏
       menubar = self.menuBar()
       self.spider_menu = menubar.addMenu('数据爬取')
       self.spider_menu.setEnabled(False)
       self.job_analysis_menu = menubar.addMenu('职位分析')
       self.job_analysis_menu.setStatusTip("职位分析")
       self.job_analysis_menu.setEnabled(False)
       self.company_analysis_menu = menubar.addMenu('公司分析')
       self.company_analysis_menu.setStatusTip("公司分析")
       self.company_analysis_menu.setEnabled(False)

       # 一级分类菜单栏
       job_ranking_menu = QMenu('排名分析',self)
       job_correlation_menu =QMenu('相关性分析',self)

       company_ranking_menu = QMenu('排名分析', self)
       company_correlation_menu = QMenu('相关性分析', self)

       # 二级分类菜单栏
       job_request_act = QAction("工作需求分析", self)
       job_request_act.triggered.connect(self.job_request)

       view_data_act = QAction(QIcon('1.png'),'观看数据',self)
       view_data_act.setStatusTip("查看数据")
       view_data_act.triggered.connect(self.view_data)

       job_rank_city_act = QAction('最多工作岗位的城市',self)
       job_rank_city_act.triggered.connect(self.job_rank_city)

       job_rank_education_act = QAction("工作对学历的要求",self)
       job_rank_education_act.triggered.connect(self.job_rank_education)

       job_rank_work_year_act = QAction("工作对经验的要求",self)
       job_rank_work_year_act.triggered.connect(self.job_rank_work_year)

       job_rank_city_money_act = QAction("平均工资最高的城市",self)
       job_rank_city_money_act.triggered.connect(self.job_rank_city_money)

       job_correlation_city_education_salary_act = QAction("哪个城市更看重学历",self)
       job_correlation_city_education_salary_act.triggered.connect(self.job_correlation_city_education_salary)

       job_correlation_city_workyear_salary_act = QAction("哪个更看重经验", self)
       job_correlation_city_workyear_salary_act.triggered.connect(self.job_correlation_city_workyear_salary)

       job_correlation_education_salary_act = QAction("学历对工资的影响", self)
       job_correlation_education_salary_act.triggered.connect(self.job_correlation_education_salary)

       job_correlation_workyear_salary_act = QAction("经验对工资的影响", self)
       job_correlation_workyear_salary_act.triggered.connect(self.job_correlation_workyear_salary)

       company_money_act = QAction('平均工资最高的公司',self)
       company_money_act.triggered.connect(self.company_money)

       company_caterogy_act=QAction("公司类型分布比例",self)
       company_caterogy_act.triggered.connect(self.company_caterogy)

       company_size_act = QAction("公司规模分布比例",self)
       company_size_act.triggered.connect(self.company_size)

       company_detail_act = QAction("公司是否融资分布比例",self)
       company_detail_act.triggered.connect(self.company_detail)

       company_type_act = QAction("公司性质分布比例",self)
       company_type_act.triggered.connect(self.company_type)

       company_date_act = QAction("公司注册时间分布比例",self)
       company_date_act.triggered.connect(self.company_date)

       # 是否融资对工资的影响
       company_detail_money_act= QAction("是否融资对工资的影响",self)
       company_detail_money_act.triggered.connect(self.company_detail_money)

       # 不同公司类型平均薪酬
       company_caterogy_money_act = QAction("不同公司类型平均薪酬", self)
       company_caterogy_money_act.triggered.connect(self.company_caterogy_money)

       # 不同公司规模平均薪酬
       company_size_money_act = QAction("不同公司规模平均薪酬", self)
       company_size_money_act.triggered.connect(self.company_size_money)

       # 不同公司详情对工资的影响
       company_type_money_act = QAction("不同公司详情对工资的影响", self)
       company_type_money_act.triggered.connect(self.company_type_money)

       # 不同注册时间对工资的影响
       company_date_money_act = QAction("不同注册时间对工资的影响", self)
       company_date_money_act.triggered.connect(self.company_date_money)

       # 不同规模的公司对学历的要求
       company_size_education_act = QAction("不同规模的公司对学历的要求", self)
       company_size_education_act.triggered.connect(self.company_size_education)

       # 不同规模的公司对经验的要求
       company_size_workyear_act = QAction("不同规模的公司对经验的要求", self)
       company_size_workyear_act.triggered.connect(self.company_size_workyear)

       #职位排名分析一级分类菜单栏添加二级分类菜单栏
       job_ranking_menu.addAction(job_rank_city_act)
       job_ranking_menu.addAction(job_rank_city_money_act)
       job_ranking_menu.addAction(job_rank_education_act)
       job_ranking_menu.addAction(job_rank_work_year_act)

       #职位相关性分析一级分类菜单栏添加二级分类菜单栏
       job_correlation_menu.addAction(job_correlation_city_education_salary_act)
       job_correlation_menu.addAction(job_correlation_city_workyear_salary_act)
       job_correlation_menu.addAction(job_correlation_education_salary_act)
       job_correlation_menu.addAction(job_correlation_workyear_salary_act)

       #公司排名分析一级分类菜单栏添加二级分类菜单栏
       company_ranking_menu.addAction(company_money_act)
       company_ranking_menu.addAction(company_caterogy_act)
       company_ranking_menu.addAction(company_size_act)
       company_ranking_menu.addAction(company_detail_act)
       company_ranking_menu.addAction(company_type_act)
       company_ranking_menu.addAction(company_date_act)

       #公司相关性分析一级分类菜单栏添加二级分类菜单栏
       company_correlation_menu.addAction(company_caterogy_money_act)
       company_correlation_menu.addAction(company_size_money_act)
       company_correlation_menu.addAction(company_type_money_act)
       company_correlation_menu.addAction(company_date_money_act)
       company_correlation_menu.addAction(company_size_education_act)
       company_correlation_menu.addAction(company_size_workyear_act)


       #爬虫菜单栏添加一级菜单栏
       self.spider_menu.addAction(view_data_act)

       # 职位分析菜单栏添加一级菜单栏
       self.job_analysis_menu.addMenu(job_ranking_menu)
       self.job_analysis_menu.addMenu(job_correlation_menu)
       self.job_analysis_menu.addAction(job_request_act)

       # 公司分析菜单栏添加一级菜单栏
       self.company_analysis_menu.addMenu(company_ranking_menu)
       self.company_analysis_menu.addMenu(company_correlation_menu)

       self.log_browser = QTextBrowser(self)
       self.log_browser.setGeometry(100, 200, 800, 350)

       #UI美化

       self.setStyleSheet("background-image:url(img/2.jpg)")

       self.show()


   def start_spider(self):
        job = str(self.text.text())
        if job =="c#":
            job ="c%23"
        elif job =="c++":
            job ="c%2B%2B"
        elif job =="C++":
            job ="C%2B%2B"
        elif job =="C#":
            job ="c%23"
        QMessageBox.about(self, '提示',"开始爬取")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.crawl_thread = CrawlThread(job)
        self.crawl_thread.start()
        self.crawl_thread.log_signal.connect(self.set_log_slot)
        self.log_browser.append('<font color="red">开始爬取</font>')
        self.text.clear()

   def job_rank_city(self):
       os.chdir('img')
       os.system('job_rank_city.html')
       os.chdir('..')

   def job_rank_education(self):
       os.chdir('img')
       os.system('job_rank_education.png')
       os.chdir('..')

   def job_rank_work_year(self):
       os.chdir('img')
       os.system('job_rank_work_year.png')
       os.chdir('..')

   def job_rank_city_money(self):
       os.chdir('img')
       os.system('job_rank_city_money.png')
       os.chdir('..')

   def job_correlation_city_education_salary(self):
       os.chdir('img')
       os.system('job_correlation_city_education_salary.png')
       os.chdir('..')

   def job_correlation_city_workyear_salary(self):
       os.chdir('img')
       os.system('job_correlation_city_workyear_salary.png')
       os.chdir('..')


   def job_correlation_education_salary(self):
       os.chdir('img')
       os.system('job_correlation_education_salary.png')
       os.chdir('..')

   def job_correlation_workyear_salary(self):
       os.chdir('img')
       os.system('job_correlation_workyear_salary.png')
       os.chdir('..')

   def view_data(self):
       os.chdir('img')
       os.system('test.csv')
       os.chdir('..')

   def job_request(self):
       os.chdir('img')
       os.system('job_request.png')
       os.chdir('..')


   def company_money(self):
       os.chdir('img')
       os.system('company_money.png')
       os.chdir('..')

   def company_caterogy(self):
       os.chdir('img')
       os.system('company_caterogy.png')
       os.chdir('..')

   def company_size(self):
       os.chdir('img')
       os.system('company_size.png')
       os.chdir('..')

   def company_detail(self):
       os.chdir('img')
       os.system('company_detail.png')
       os.chdir('..')


   def company_type(self):
       os.chdir('img')
       os.system('company_type.png')
       os.chdir('..')

   def company_date(self):
       os.chdir('img')
       os.system('company_date.png')
       os.chdir('..')

   def company_detail_money(self):
       os.chdir('img')
       os.system('company_detail_money.png')
       os.chdir('..')

   def company_caterogy_money(self):
       os.chdir('img')
       os.system('company_caterogy_money.png')
       os.chdir('..')

   def company_size_money(self):
       os.chdir('img')
       os.system('company_size_money.png')
       os.chdir('..')

   def company_type_money(self):
       os.chdir('img')
       os.system('company_type_money.png')
       os.chdir('..')

   def company_date_money(self):
       os.chdir('img')
       os.system('company_date_money.png')
       os.chdir('..')

   def company_size_education(self):
       os.chdir('img')
       os.system('company_size_education.png')
       os.chdir('..')

   def company_size_workyear(self):
       os.chdir('img')
       os.system('company_size_workyear.png')
       os.chdir('..')

   def stop_spider(self):
       self.stop_btn.setEnabled(False)
       self.start_btn.setEnabled(True)
       self.analysis_btn.setEnabled(True)
       self.spider_menu.setEnabled(True)
       self.crawl_thread.fp.close()
       self.crawl_thread.terminate()

   def analysis(self):
        QMessageBox.about(self, '提示',"分析需要些时间")
        self.text.clear()
        analysis.analysis()
        self.log_browser.append('<font color="red">分析好了</font>')
        self.job_analysis_menu.setEnabled(True)
        self.company_analysis_menu.setEnabled(True)

   def set_log_slot(self, new_log):
       self.log_browser.append(new_log)

   def closeEvent(self, event):

       reply = QMessageBox.question(self, '确认', '确认退出吗',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
       if reply == QMessageBox.Yes:
           event.accept()
       else:
           event.ignore()





