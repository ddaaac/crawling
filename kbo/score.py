import os
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

score_df = pd.read_csv('score.csv', encoding='cp949')
print(score_df.columns)


def get_score_by_month(month):
    url = "https://sports.news.naver.com/kbaseball/schedule/index.nhn?date=20190604&month=%s&year=2018&teamCode=" \
            % month
    path = os.path.join("C:\\", "Users", "skybl", "Downloads", "chromedriver.exe")
    browser = webdriver.Chrome(path)
    browser.get(url)
    try:
        table = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tb_wrap"))
        )

    finally:
        rows = table.find_elements_by_xpath("div")
        for idx, row in enumerate(rows):
            scores = row.find_elements_by_xpath("table/tbody/tr")
            date = scores[0].find_elements_by_xpath("td/span[@class='td_date']/strong")
            if date:
                print(date[0].text)

            for score in scores:
                td_score = score.find_elements_by_xpath("td/strong[@class='td_score']")
                if td_score and td_score[0].text != 'VS':
                    lr_score = td_score[0].text
                    lr_score = lr_score.split(':')
                    print(td_score[0].text)
                else:
                    continue

                team_lft = score.find_elements_by_xpath("td/span[@class='team_lft']")
                if team_lft:
                    print(team_lft[0].text)

                team_rgt = score.find_elements_by_xpath("td/span[@class='team_rgt']")
                if team_rgt:
                    print(team_rgt[0].text)
                score_df.loc[len(score_df)] = [team_rgt[0].text, lr_score[0], team_lft[0].text, lr_score[1], str(date[0].text)]
                print()
    score_df.to_csv('score.csv', encoding='cp949', mode='w')

# d = datetime.datetime(2018, 3, 1)
d = datetime.datetime(2018, 10, 1)
while True:
    get_score_by_month(d.strftime("%m"))
    # d += datetime.timedelta(days=32)
    # if d.strftime("%m") == '11':
    #     break
