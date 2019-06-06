import pandas as pd
import datetime

batter = pd.read_csv('batter.csv', encoding='cp949', index_col=['날짜', '팀명'])
pitcher = pd.read_csv('pitcher.csv', encoding='cp949', index_col=['날짜', '팀명'])
score = pd.read_csv('score.csv', encoding='cp949')

data = pd.DataFrame()

for row_index, row in score.iterrows():
    [date, team1, score1, team2, score2] = row
    date = (datetime.datetime.strptime(date, "%Y-%m-%d").date() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        team1_batter = batter.loc[(date, team1), :]
        team1_batter = team1_batter.reset_index(drop=True)
        team2_pitcher = pitcher.loc[(date, team2), :]
        team2_pitcher = team2_pitcher.reset_index(drop=True)

        team2_batter = batter.loc[(date, team2), :]
        team2_batter = team2_batter.reset_index(drop=True)
        team1_pitcher = pitcher.loc[(date, team1), :]
        team1_pitcher = team1_pitcher.reset_index(drop=True)
    except KeyError:
        continue

    team1_get_score = team1_batter.join(team2_pitcher)
    team1_get_score['label'] = score1
    data = data.append(team1_get_score)

    team2_get_score = team2_batter.join(team1_pitcher)
    team2_get_score['label'] = score2
    data = data.append(team2_get_score)

data.to_csv("data.csv", encoding='cp949')

