#@source https://www.fantasyfootballdatapros.com/blog/intermediate/27

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from traitlets.traitlets import Bytes; sns.set_style('whitegrid');
import numpy as np
import requests
from io import BytesIO
import nflfastpy
from IPython.display import display

frame = nflfastpy.load_pbp_data(year = 2021)
team_frame = nflfastpy.load_team_logo_data()

passes_frame = frame.loc[frame['pass_attempt'] == 1, ['receiver_player_id', 'posteam', 'receiver_player_name', 'receiver_jersey_number',
                                              'air_yards', 'complete_pass', 'yards_gained', 'pass_touchdown']]

passes_frame['ppr_receiving_fantasy_points'] = passes_frame['complete_pass'] + 6*passes_frame['pass_touchdown'] + 0.1*passes_frame['yards_gained']

team_frame = team_frame.rename({'team_abbr': 'posteam'}, axis= 1)

passes_frame = passes_frame.merge(team_frame, how = 'left', on = 'posteam')

top_player_fp = passes_frame[['receiver_player_id', 'ppr_receiving_fantasy_points']].groupby('receiver_player_id', as_index=False)\
.sum().sort_values(by='ppr_receiving_fantasy_points', ascending=False)[:10]

passes_frame = passes_frame.loc[passes_frame['receiver_player_id'].isin(top_player_fp['receiver_player_id'])]

passes_frame = passes_frame.dropna()

passes_frame = passes_frame[['receiver_player_id', 'receiver_player_name', 'air_yards', 'team_color', 'team_logo_wikipedia']]

passes_frame.head()

passes_frame['receiver_player_name'].unique()

roster_frame = nflfastpy.load_roster_data(2021)

roster_frame['receiver_player_name'] = roster_frame['full_name'].apply(lambda x: '.'.join([x.split()[0][0], x.split()[-1]]))

roster_frame = roster_frame.loc[(roster_frame['season'] == 2021) & (roster_frame['gsis_id'].isin(passes_frame['receiver_player_id'].unique())) \
                          & (roster_frame['position'].isin(['WR', 'TE', 'RB'])), 
                          ['receiver_player_name', 'position', 'full_name', 'headshot_url']]

roster_frame = roster_frame.reset_index(drop = True)

with pd.option_context('display.max_rows', None):
    display(roster_frame)

passes_frame = passes_frame.merge(roster_frame, on='receiver_player_name', how='left').drop(['full_name', 'position'], axis=1)

passes_frame.head()

#function part

subset = [subset for subset in passes_frame.groupby('receiver_player_id')]

fig, axes = plt.subplots(5, 2, figsize = (13, 15))

rows, columns = axes.shape[0], axes.shape[1]
i = 0

for row in range(rows):
    for col in range(columns):
        player_frame = subset[i][-1]
        player_name = player_frame['receiver_player_name'].values[0]
        primary_color = player_frame['team_color'].values[0]
        headshot_url = player_frame['headshot_url'].values[0]

        res = requests.get(headshot_url)
        img = plt.imread(BytesIO(res.content))

        ax = sns.kdeplot(player_frame['air_yards'], ax = axes[row, col], label=player_name, color=primary_color)
        ax.set_xlim(-5)
        lines = ax.get_lines()[0].get_xydata()
        x, y = lines[:, 0], lines[:, 1]

        ax.imshow(img, extent=[75, 100, 0, 0.03], aspect='auto', zorder=1000)
        ax.fill_between(x, y, color=primary_color, alpha=0.4)
        ax.set_xticks(range(0, 101, 10))
        ax.set_yticks(np.linspace(0, 0.07, 10))
        ax.set_xlabel('Air Yards')
        ax.set_ylabel('Density')

        ax.legend()

        i += 1
print("bruh")
plt.tight_layout()
plt.show()