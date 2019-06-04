import bq_helper

baseball = bq_helper.BigQueryHelper(active_project="bigquery-public-data", dataset_name="baseball")

col = ['gameId', 'startTime', 'gameStatus', 'attendance', 'dayNight', 'durationMinutes',
       'awayTeamName', 'homeTeamName', 'venueName', 'venueSurface', 'venueCity', 'venueState',
       'homeFinalRuns', 'homeFinalHits', 'homeFinalErrors', 'awayFinalRuns', 'awayFinalHits', 'awayFinalErrors',
       'inningNumber', 'inningHalf', 'description', 'atBatEventSequenceNumber', 'outcomeDescription',
       'hitterLastName', 'hitterBatHand', 'pitcherLastName', 'pitcherThrowHand', 'pitchTypeDescription',
       'pitchSpeed', 'balls', 'strikes', 'outs']
col_field = ''
for c in col:
    col_field += c + ','
col_field = col_field[:-1]
print(col_field)
query = """SELECT %s
            FROM `bigquery-public-data.baseball.games_wide`
             """
games = baseball.query_to_pandas_safe(query % col_field)
print(games)
games.to_csv('new_games.csv', mode='w')


