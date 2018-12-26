from plotly.graph_objs import Scatter, Layout
import plotly
import plotly.offline as py
import numpy as np
import plotly.graph_objs as go
import jieba.analyse
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import re

from db_util import get_data, execute


def analyse_academy():
    sql_academy = "SELECT student_major, COUNT(*) from project GROUP BY student_major ORDER BY COUNT(*) DESC"
    academy_data = execute(sql_academy)
    academy_dict = {}
    for index in range(len(academy_data)):
        name = academy_data[index][0]
        value = academy_data[index][1]
        academy_dict[name] = value
    trace0 = go.Bar(
        x= list(academy_dict.keys()),
        y= list(academy_dict.values()),
        name = '毕业人数',
        marker = dict(
            color = 'rgb(0,229,238)'
        )
    )
    sql_male = "SELECT student_major, COUNT(*) from project WHERE student_gender = '男' GROUP BY student_major ORDER BY COUNT(*) DESC"
    male_data = execute(sql_male)
    male_dict = {}
    for index in range(len(male_data)):
        name = male_data[index][0]
        value = male_data[index][1]
        male_dict[name] = value
    trace1 = go.Bar(
        x= list(male_dict.keys()),
        y= list(male_dict.values()),
        name = '男生人数',
        marker = dict(
            color = 'rgb(255,185, 15)'
        )
    )
    sql_female = "SELECT student_major, COUNT(*) from project WHERE student_gender = '女' GROUP BY student_major ORDER BY COUNT(*) DESC"
    female_data = execute(sql_female)
    female_dict = {}
    for index in range(len(female_data)):
        name = female_data[index][0]
        value = female_data[index][1]
        female_dict[name] = value
    trace2 = go.Bar(
        x=list(female_dict.keys()),
        y=list(female_dict.values()),
        name='女生人数',
        marker=dict(
            color='rgb(255,69,0)'
        )
    )
    data = [trace0, trace1, trace2]
    py.plot(data)
    return None

def analyse_project_teacher():
    sql = "SELECT teacher_name, COUNT(*) from project GROUP BY teacher_name ORDER BY COUNT(*) DESC"
    teacher_data = execute(sql)[0:20]
    teacher_dict = {}
    for index in range(len(teacher_data)):
        name = teacher_data[index][0]
        value = teacher_data[index][1]
        teacher_dict[name] = value
    trace0 = go.Bar(
        x=list(teacher_dict.keys()),
        y=list(teacher_dict.values()),
        name='指导人数',
        marker=dict(
            color='rgb(100,149,237)'
        )
    )
    data = [trace0]
    py.plot(data)
    return None

def analyse_project_student_name():
    sql = "SELECT student_name, COUNT(*) from project GROUP BY student_name ORDER BY COUNT(*) DESC LIMIT 68"
    student_name_data = execute(sql)
    student_name_dict = {}
    for index in range(len(student_name_data)):
        name = student_name_data[index][0]
        value = student_name_data[index][1]
        student_name_dict[name] = value

    male_dict = {}
    female_dict = {}
    for name in student_name_dict.keys():
        sql_male = "SELECT COUNT(*) from project WHERE student_name = %s AND student_gender = '男'" % ("'"+name+"'")
        sql_female = "SELECT COUNT(*) from project WHERE student_name = %s AND student_gender = '女'" % ("'"+name+"'")
        male_data = execute(sql_male)
        female_data = execute(sql_female)
        male_dict[name] = male_data[0][0]
        female_dict[name] = female_data[0][0]

    trace0 = go.Bar(
        x=list(male_dict.keys()),
        y=list(male_dict.values()),
        name='男',
        marker=dict(
            color='rgb(100,149,237)'
        )
    )

    trace1 = go.Bar(
        x=list(female_dict.keys()),
        y=list(female_dict.values()),
        name='女',
        marker=dict(
            color='rgb(238,44,44)'
        )
    )

    data = [trace0,trace1]
    layout = go.Layout(
        barmode='stack'
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='stacked-bar')

def analyse_project_type_and_property():
    sql_type = "SELECT project_type, COUNT(*) from project GROUP BY project_type ORDER BY COUNT(*) DESC LIMIT 5"
    type_data = execute(sql_type)
    type_dict = {}
    for index in range(len(type_data)):
        name = type_data[index][0]
        value = type_data[index][1]
        type_dict[name] = value
    trace0 = go.Bar(
        x= list(type_dict.keys()),
        y= list(type_dict.values()),
        name = '课题类型',
        marker = dict(
            color = 'rgb(139,10,80)'
        )
    )

    sql_property = "SELECT project_property, COUNT(*) from project GROUP BY project_property ORDER BY COUNT(*) DESC LIMIT 6"
    property_data = execute(sql_property)
    property_dict = {}
    for index in range(len(property_data)):
        name = property_data[index][0]
        value = property_data[index][1]
        property_dict[name] = value
    trace1 = go.Bar(
        x=list(property_dict.keys()),
        y=list(property_dict.values()),
        name='课题性质',
        marker=dict(
            color='rgb(255,228,225)'
        )
    )

    data = [trace0, trace1]
    py.plot(data)
    return None

def annlyse_project_title(academy, stopword, img_url):
    path = r'C:\Users\casua\Desktop\新建文件夹'
    font = r'C:/Windows/Fonts/STKAITI.ttf'
    sql = "SELECT project_name FROM project WHERE student_major = %s " % academy
    data = execute(sql)
    words = {}
    # for title in list(data):
    #     for w, c in jieba.analyse.extract_tags(str(title), withWeight=True):
    #         try:
    #             words[w] = words[w] + float(c)
    #         except:
    #             words[w] = float(c)


    wash_signature = []
    a= list(data)
    print(list(a))
    for title in list(data):
        rep = re.compile("1f\d+\w*|[<>/=【】『』♂ω]")
        item = rep.sub("", title[0])
        wash_signature.append(item)

    words = "".join(wash_signature)
    wordlist = jieba.cut(words, cut_all=True)
    rst = " ".join(wordlist)
    print(len(rst))
    img = Image.open(path + img_url)
    img_array = np.array(img)
    wc = WordCloud(
        background_color='white',
        width=1000,
        height=800,
        mask=img_array,
        font_path=font,
        stopwords=stopword
    )
    wc.generate_from_text(rst)  # 绘制图片
    plt.imshow(wc)
    plt.axis('off')
    plt.figure()
    plt.show()  # 显示图片
    wc.to_file(path + r'\new.png')  # 保存图片
    return None


if __name__ == '__main__':
    # data = analyse_academy()
    # analyse_project_teacher()
    # analyse_project_student_name()
    # analyse_project_type_and_property()
    cs_stopword = ['基于', '设计', '实现', '管理系', '管理', '管理系统']
    cs_img_url = r'\photo-1527443154391-507e9dc6c5cc.jpg'
    cs_name = "'"+'计算机科学与工程学院'+"'"

    ee_stopword = ['基于','设计','控制','系统']
    ee_img_url = r'\photo-1527443154391-507e9dc6c5cc.jpg'
    ee_name = "'" + '电子信息学院' + "'"

    ec_stopword = ['设计','研究','XXX','XX']
    ec_img_url = r'\photo-1527443154391-507e9dc6c5cc.jpg'
    ec_name = "'" + '经济管理学院' + "'"

    cl_stopword = ['研究','设计']
    cl_img_url = r'\photo-1527443154391-507e9dc6c5cc.jpg'
    cl_name = "'" + '材料科学与工程学院' + "'"

    cb_stopword = ['研究']
    cb_img_url = r'\photo-1527443154391-507e9dc6c5cc.jpg'
    cb_name = "'" + '船舶与海洋工程学院' + "'"

    annlyse_project_title(cl_name, cl_stopword, cl_img_url)