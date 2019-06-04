import os
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_date = '2018-03-24'
names = ['SK', 'NC', 'Hero', '두산', 'KT', 'KIA', 'LG', '삼성', '한화', '롯데']

# batter = pd.DataFrame()
# pitcher = pd.DataFrame()
batter = pd.read_csv('batter.csv', encoding='cp949')
pitcher = pd.read_csv('pitcher.csv', encoding='cp949')
error_date = []


def get_data(table, team):
    # 첫 행은 columns의 이름으로 사용
    first_row = table.find_element_by_tag_name("tr")
    columns = str(first_row.text[2:]).split(' ')
    # 다음 행부터는 데이터가 담겨있음
    rows = table.find_elements_by_xpath("//tbody/tr")
    for idx, row in enumerate(rows):
        if idx == 0:
            continue
        elif idx > 10:
            break
        data = row.find_elements_by_xpath("td")[1:]
        team_name = data[0].text
        for index, d in enumerate(data):
            team[team_name][columns[index]] = d.text
    return team


def get_data_by_date(date):
    global batter, pitcher
    type = ['main', 'standard', 'advanced']
    position = ['pitcher/', '']
    for p in position:
        team = {}
        for name in names:
            team[name] = {'날짜': date}
        for t in type:
            url = "http://www.kbreport.com/teams/%s%s?teamId=&defense_no=&" \
            "year_from=%s&year_to=%s&split01=day&split02_1=%s&split02_2=%s" \
            % (p, t, start_date[:4], date[:4], start_date, date)
            # print(url)
            path = os.path.join("C:\\", "Users", "skybl", "Downloads", "chromedriver.exe")
            browser = webdriver.Chrome(path)
            browser.get(url)
            try:
                table = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ltb-table"))
                )

            finally:
                # 첫 행은 columns의 이름으로 사용
                first_row = table.find_element_by_tag_name("tr")
                columns = str(first_row.text[2:]).split(' ')
                # 다음 행부터는 데이터가 담겨있음
                rows = table.find_elements_by_xpath("//tbody/tr")
                for idx, row in enumerate(rows):
                    if idx == 0:
                        continue
                    elif idx > 10:
                        break
                    data = row.find_elements_by_xpath("td")[1:]
                    team_name = data[0].text
                    for index, d in enumerate(data):
                        team[team_name][columns[index]] = d.text
            if not table:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ERROR@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                error_date.append(date)
            browser.quit()
        df = pitcher if p else batter
        for key in team:
            df = df.append(team[key], ignore_index=True)
        if p:
            pitcher = df
        else:
            batter = df
    print(date, " 끝")


def get_one_season():
    date = datetime.datetime(2018, 7, 26)
    print(date)

    while True:
        get_data_by_date(date.strftime("%Y-%m-%d"))
        date += datetime.timedelta(days=1)
        if date == datetime.datetime(2018, 10, 14):
            break
        batter.to_csv('batter.csv', mode='w', encoding='cp949')
        pitcher.to_csv('pitcher.csv', mode='w', encoding='cp949')


get_one_season()
print("error date: ", error_date)
