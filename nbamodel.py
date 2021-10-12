#@source https://github.com/SimplePy/NBA_api_regression

import pandas as pd
import numpy as np
from sklearn import linear_model
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt

# get league leaders module
data = endpoints.leagueleaders.LeagueLeaders()
# create data frame
data_df = data.league_leaders.get_data_frame()

# data frame head
data_df.head()

attempt_avg, points_avg = data_df.FGA/data_df.GP, data_df.PTS/data_df.GP

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
plt.title('NBA FGA and PPG')
plt.xlabel('FGA per Game')
plt.ylabel('Points per Game')
plt.text(10, 25, f'R2 = {r2}') # coord of text

plt.annotate(data_df.PLAYER[0], 
            (attempt_avg[0], points_avg[0]),
             (attempt_avg[0] - 7, points_avg[0] - 2),
             arrowprops = dict(arrowstyle = '-'))

plt.savefig('graph_1.png', dpi = 300)

