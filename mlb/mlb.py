from bs4 import BeautifulSoup
import os
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = 'https://www.mlb.com/scores/2016-02-17'
df = pd.DataFrame(columns=["date", "team1", "score1", "team2", "score2"])


def get_scores(url):
    path = os.path.join("C:\\", "Users", "skybl", "Downloads", "chromedriver.exe")
    browser = webdriver.Chrome(path)
    browser.get(url)
    try:
        element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "container"))
        )

    finally:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        score_areas = soup.find('div', {"class": "l-grid__content l-grid__content--none"})
        score_areas = score_areas.find('section')
        score_area = score_areas.find_all('li', {"class": "mlb-scores__list-item mlb-scores__list-item--game"})
        for area in score_area:
            names = area.find_all("span", {"class": "g5-component--mlb-scores__team__info__name--long"})
            scores = area.find_all("td", {"class": "g5-component--mlb-scores__linescore__table--summary__cell g5-component--mlb-scores__linescore__table--summary__cell--runs"})
            df.loc[len(df)] = [url[-5:] , names[0].text.strip(), scores[0].text.strip(), names[1].text.strip(), scores[1].text.strip()]
        if not score_area:
            return 1
        print(df)
        browser.quit()
    return 0


def year_score():
    url = 'https://www.mlb.com/scores/'
    date = datetime.datetime(2016, 4, 4)
    while True:
        URL = url + date.strftime("%Y-%m-%d")
        cnt = 0
        while get_scores(URL) and cnt < 5:
            print("error at ", date)
            cnt += 1
        if date == datetime.datetime(2016, 10, 3):
            break
        date += datetime. timedelta(days=1)
        df.to_csv("total_score.csv", mode='w')


year_score()
