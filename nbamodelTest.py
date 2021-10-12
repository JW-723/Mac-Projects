
import pandas as pd
import numpy as np
from sklearn import linear_model
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt

# get league leaders module
playerid = '203076'
data = endpoints.playercareerstats.PlayerCareerStats(player_id=playerid)
# create data frame
data_df = data.get_data_frames()[0]

# data frame head
data_df.head()

attempt_avg, points_avg = data_df.FGA/data_df.GP, data_df.PTS/data_df.GP
seasons = data_df.SEASON_ID
seasons_ids = seasons.values.tolist()
print(seasons_ids)

attempt_avg = np.array(attempt_avg).reshape(-1, 1)
points_avg = np.array(points_avg).reshape(-1, 1)

model_1 = linear_model.LinearRegression()
model_1.fit(attempt_avg, points_avg)

# r2 value then predicting off of input
r2 = round(model_1.score(attempt_avg, points_avg), 2)
predictions_1 = model_1.predict(attempt_avg)

# graphing part
plt.scatter(attempt_avg, points_avg, s = 15, alpha = 0.5)
plt.plot(attempt_avg, predictions_1, color = 'black')
plt.title('NBA Player id' + playerid)
plt.xlabel('FGA per Game')
plt.ylabel('Points per Game')
#plt.text(10, 25, f'R2 = {r2}') # coord of text

for i, txt in enumerate(seasons_ids):
    plt.annotate(txt, (attempt_avg[i], points_avg[i]))



plt.savefig('graph_1.png', dpi = 300)

