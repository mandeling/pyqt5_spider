import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from wordcloud import WordCloud
import jieba
from pyecharts import Geo


mpl.rcParams['font.sans-serif'] = ['SimHei']
def analysis():
    df = pd.read_csv('img/test.csv', encoding='utf-8')
    df = df[~df['name'].isin(['name'])]
    df['salary_low'], df['salary_high'] = df['salary'].str.split('-', 1).str

    # 取工资下限
    df['salary_low'] = (df['salary_low']).astype(int) * 1000
    # 取工资上限
    df['salary_high'] = (df['salary_high'].str.split('K').str[0]).astype(int) * 1000

    # 取工资平均值
    df['salary_average'] = (df['salary_low'] + df['salary_high']) / 2
    # 取掉工资异常值
    df_all = df[df.salary_low < 100000]


    """
    
        职位排名分析
        
    """
    # 按地区工作个数来排序

    data1 = df_all['city'].value_counts().index.tolist()
    data2 = df_all['city'].value_counts().tolist()
    data =list(zip(data1,data2))

    geo = Geo("工作岗位需求图",  title_color="#fff", title_pos="center", width=1200, height=600,
              background_color='#404a59')

    attr, value = geo.cast(data)
    geo.add("工作岗位需求图", attr, value, visual_range=[0, 3], type='heatmap', visual_text_color="#fff", symbol_size=15,
            is_visualmap=True, is_roam=False)
    geo.render(path="img/job_rank_city.html")



    # 按工作经验来排序
    plt.figure(figsize=(8, 8))
    df_all['work_years'].value_counts().plot.pie(subplots=True, autopct='%.0f%%')
    plt.title('工作经验的要求')
    plt.savefig('img/job_rank_work_year.png')
    plt.close()

    # 按学历学位来排序
    plt.figure(figsize=(8, 8))
    df_all['education'].value_counts().plot.pie(subplots=True,  autopct='%.0f%%')
    plt.title('学历要求')
    plt.savefig('img/job_rank_education.png')
    plt.close()

    # 不同地区薪资高低来排序
    plt.figure(figsize=(6, 7))
    df_all.groupby('city').mean()['salary_average'].sort_values(ascending=False).head(10).plot.bar()
    plt.title('平均薪水最多的前10个地区')
    plt.savefig('img/job_rank_city_money.png')
    plt.close()





    """

         职位相关性分析

    """

    # 经验对工资的影响
    plt.figure(figsize=(6, 7))
    df_all.groupby('work_years').mean()['salary_average'].sort_values(ascending=False).head(10).plot.bar()
    plt.title('不同经验薪资高低来排序')
    plt.savefig('img/job_correlation_workyear_salary.png')
    plt.close()

    # 学历对工资的影响
    plt.figure(figsize=(6, 7))
    df_all.groupby('education').mean()['salary_average'].sort_values(ascending=False).plot.bar()
    plt.title('不同学历对薪酬的关系')
    plt.savefig('img/job_correlation_education_salary.png')
    plt.close()

    # 哪个城市更看重学历
    plt.figure(figsize=(6, 7) )
    citys = df_all['city'].value_counts().head(10)
    df_city = df_all[df_all.city.isin(list(citys.keys()))]
    df_city.groupby(['city', 'education']).mean()['salary_average'].unstack().plot.bar()
    plt.title('哪个城市更看重学历')
    plt.savefig('img/job_correlation_city_education_salary.png')
    plt.close()

    # 哪个城市更看重经验
    plt.figure(figsize=(6, 7)  )
    df_city.groupby(['city', 'work_years']).mean()['salary_average'].unstack().plot.bar()
    plt.title('不同地区对经验薪资高低来排序' )
    plt.savefig('img/job_correlation_city_workyear_salary.png')
    plt.close()





    """

        公司排名分析

    """
    # 按公司类型来分布
    plt.figure(figsize=(6, 7))
    df_company=df_all[df_all.duplicated('company')==False]
    df_company['company_caterogy'].value_counts().plot.pie(subplots=True, autopct='%.0f%%')
    plt.title('公司类型的分布')
    plt.savefig('img/company_caterogy.png')
    plt.close()

    # 按公司规模来分布
    plt.figure(figsize=(8, 8))
    df_company['company_size'].value_counts().plot.pie(subplots=True, autopct='%.0f%%')
    plt.title('公司规模大小的分布')
    plt.savefig('img/company_size.png')
    plt.close()

    # 按公司详情来排序
    plt.figure(figsize=(8,8))
    df_company['company_detail'].value_counts().plot.pie(subplots=True, autopct='%.0f%%')
    plt.title('公司是否需要融资比例')
    plt.savefig('img/company_detail.png')
    plt.close()

    #公司性质分布
    plt.figure(figsize=(10, 10))
    df_company['company_type'].value_counts().plot.pie(subplots=True, autopct='%.0f%%')
    plt.title('公司性质比例')
    plt.savefig('img/company_type.png')
    plt.close()

    #公司注册时间分布
    plt.figure(figsize=(8, 8))
    df_company['new_date'] = df_company.company_date.str.split('-', expand=True)[0]
    df_company['new_date'].value_counts().plot.pie(subplots=True,autopct='%.0f%%')
    plt.title('公司成立时间比例')
    plt.savefig('img/company_date.png')
    plt.close()

    # 不同公司薪资高低来排序
    plt.figure(figsize=(6, 7))
    df_all.groupby('company').mean()['salary_average'].sort_values(ascending=False).head(10).plot.bar()
    plt.title('平均薪水最多的前10个公司')
    plt.savefig('img/company_money.png')
    plt.close()


    """

        公司相关性分析

    """
    # 是否融资对薪酬的关系
    plt.figure(figsize=(6, 7))
    df_all.groupby('company_detail').mean()['salary_average'].sort_values(ascending=False).plot.bar()
    plt.title('是否融资对薪酬的关系')
    plt.savefig('img/company_detail_money.png')
    plt.close()

    # 各种公司类型的薪酬的关系
    plt.figure(figsize=(6, 8))
    df_all.groupby('company_caterogy').mean()['salary_average'].sort_values(ascending=False).plot.bar()
    plt.title('各种公司类型的薪酬的关系')
    plt.savefig('img/company_caterogy_money.png')
    plt.close()

    # 不同公司规模对薪酬的关系
    plt.figure(figsize=(6, 8))
    df_all.groupby('company_size').mean()['salary_average'].sort_values(ascending=False).plot.bar()
    plt.title('不同公司规模对薪酬的关系')
    plt.savefig('img/company_size_money.png')
    plt.close()

    #不同公司详情对工资的影响
    plt.figure(figsize=(6, 13))
    df_all.groupby('company_type').mean()['salary_average'].sort_values(ascending=False).plot.bar()
    plt.title('不同公司详情对工资的影响')
    plt.savefig('img/company_type_money.png')
    plt.close()

    #不同注册时间对工资的影响
    plt.figure(figsize=(6, 8))
    df_all['new_date'] = df_all.company_date.str.split('-', expand=True)[0]
    df_all.groupby('new_date').mean()['salary_average'].sort_values(ascending=False).plot.bar()
    plt.title('不同注册时间对工资的影响')
    plt.savefig('img/company_date_money.png')
    plt.close()

    #不同规模的公司对学历的要求

    plt.figure( )
    df_all.groupby(['company_size', 'education']).mean()['salary_average'].unstack().plot.bar()
    plt.title('不同规模的公司对学历的要求')
    plt.savefig('img/company_size_education.png')
    plt.close()
    #不同规模的公司对经验的要求

    plt.figure( )
    df_all.groupby(['company_size', 'work_years']).mean()['salary_average'].unstack().plot.bar()
    plt.title('不同规模的公司对经验的要求' )
    plt.savefig('img/company_size_workyear.png')
    plt.close()

    """
        职位需求分析

    """



    # 词云图
    font_path = r'C:\Windows\Fonts\simhei.ttf'

    stopwords = ('有限公司','熟悉', '开发', '具备', '具有', '优先', '岗位职责', '要求', '职责', '以上', '熟练掌握', '语言')
    wc = WordCloud(
        scale=1,  # 缩放2倍
        collocations=False,
        font_path=font_path,
        max_font_size=100,
        width=800,
        height=600,
        stopwords=stopwords,
        background_color='#383838',  # 灰色
        colormap='Blues')

    # 全语言词云图
    word_list_all = list(df_all['job_request'])
    word_all = ''
    for s in word_list_all:
        word_all = word_all + s + ' '

    word_all.encode('utf-8')
    word_all += ' '.join(jieba.cut(word_all, cut_all=False))
    wc.generate(word_all)

    word_all = WordCloud.process_text(wc, word_all)
    sort = sorted(word_all.items(), key=lambda e: e[1], reverse=True)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('img/job_request.png')
    plt.close()
