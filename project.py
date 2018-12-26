from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from db_util import save_project_info


def setup():
    chromePath = r'C:\Users\x\Downloads\chromedriver_win32\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=chromePath)
    return browser

def login(username, password, browser):
    browser.get("http://x.x.edu.cn/index.aspx")
    user_btn = browser.find_element_by_id("UserId")
    pwd_btn = browser.find_element_by_id("Pwd")
    submit_btn = browser.find_element_by_id("LoginButton")

    user_btn.send_keys(username)
    pwd_btn.send_keys(password)
    submit_btn.send_keys(Keys.ENTER)

    return browser

def set_sessions(browser):
    request = requests.Session()
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    request.headers.update(headers)
    cookies = browser.get_cookies()
    current_url = browser.current_url
    for cookie in cookies:
        request.cookies.set(cookie['name'], cookie['value'])
    return request,current_url

def get_project_data(content):
    soup = BeautifulSoup(content, "html.parser")
    try:
        trs = soup.find('div', attrs={'id': 'Panel2'}).find_all('tr')
        tds = trs[1].find_all('td')
    except:
        return
    project_name = "".join(tds[0].text.split())
    project_type = "".join(tds[1].text.split())
    project_property = "".join(tds[2].text.split())
    student_name = "".join(tds[3].text.split())
    return project_name, project_type, project_property, student_name

def get_df():
    df = pd.read_excel(r'C:\Users\casua\Desktop\data.xls')
    return df

def get_num_list(df):
    student_num_list = df['学号'].unique()
    return student_num_list

def get_row(student_num, df):
    row = df[df['学号'].isin([student_num])]
    return row.values[0]

if __name__ == "__main__":
    df = get_df()
    num_list = get_num_list(df)
    for num in num_list:
        # read
        row = get_row(num, df)
        student_academy = row[3]
        student_major = row[4]
        student_num = row[6]
        student_name = row[7]
        student_gender = row[8]
        # crawl
        browser = login(student_num, student_num, setup())
        try:
            rq, url = set_sessions(browser)
        except:
            browser.close()
            continue
        browser.close()
        sid = url[39:]
        try:
            result = rq.get("http://x.x.edu.cn/x/x.aspx" + "?" + sid)
        except:
            continue
        result.encoding = "GB2312"
        info_list = get_project_data(result.content)
        print(info_list)
        # save
        try:
            save_project_info(info_list[0], info_list[1], info_list[2], student_name, student_num, student_academy, student_major, student_gender, info_list[3])
        except:
            continue