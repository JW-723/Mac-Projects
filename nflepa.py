#@source https://www.fantasyfootballdatapros.com/blog/intermediate/26
 
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
import nflfastpy as nfl
import requests
from io import BytesIO

frame = nfl.load_pbp_data(2021)

frame.head(5)

epa_df = pd.DataFrame({
    'offense_epa': frame.groupby('posteam')['epa'].sum(),
    'offense_plays': frame['posteam'].value_counts(), 
})

epa_df['offense_epa/play'] = epa_df['offense_epa'] / epa_df['offense_plays']

epa_df.sort_values(by = 'offense_epa/play', ascending = False).head()

epa_df['defense_epa'] = frame.groupby('defteam')['epa'].sum()
epa_df['defense_plays'] = frame['defteam'].value_counts()
epa_df['defense_epa/play'] = epa_df['defense_epa'] / epa_df['defense_plays']

epa_df.sort_values(by = 'defense_epa/play', ascending = False).head()

schedule = nfl.load_schedule_data(year = 2021)

def get_opponent(opp):
    team = schedule[(schedule['away_team']==opp) | (schedule['home_team']==opp)]
    opponent = team[['week', 'home_team']].where(team.away_team == opp, team[['week', 'away_team']].values)
    return opponent.rename(columns={'home_team':'opp_team'})
# original function
def opponent_epa(team):
    opponent = get_opponent(team)
    epa_opponent = epa_df.reset_index().rename(columns={'index':'opp_team'})
    return opponent.merge(epa_opponent, on = 'opp_team').loc[:,['week',
                                                                'opp_team',
                                                                'offense_epa/play',
                                                                'defense_epa/play']].sort_values(by='week')

def past_future_opp_epa(team, weeks):
    opp_epa = opponent_epa(team)
    past_games = opp_epa[opp_epa['week'] <= weeks].loc[:,['offense_epa/play','defense_epa/play']].mean()
    future_games = opp_epa[opp_epa['week'] > weeks].loc[:,['offense_epa/play','defense_epa/play']].mean()
    return past_games, future_games

def delta_epa_offense(team,weeks):
    offense_past = past_future_opp_epa(team, weeks)[0]['offense_epa/play']
    offense_future = past_future_opp_epa(team, weeks)[1]['offense_epa/play']
    offense_delta = offense_future - offense_past
    return offense_delta

def delta_epa_defense(team,weeks):
    defense_past = past_future_opp_epa(team, weeks)[0]['defense_epa/play']
    defense_future = past_future_opp_epa(team, weeks)[1]['defense_epa/play']
    defense_delta = defense_future - defense_past
    return defense_delta

team = []
offense_delta = []
defense_delta = []

for x in epa_df.index:
    team.append(x)
    offense_delta.append(delta_epa_offense(x, 18))
    defense_delta.append(delta_epa_defense(x, 18))

schedule_epa = pd.DataFrame()
schedule_epa['Team'] = team
schedule_epa['Offense_EPA_Delta'] = offense_delta
schedule_epa['Defense_EPA_Delta'] = defense_delta

schedule_epa.sort_values(by='Defense_EPA_Delta').head()

#Original Plotting
plt.style.use('ggplot')

schedule_epa = schedule_epa.set_index('Team')
x = schedule_epa['Offense_EPA_Delta'].values
y = schedule_epa['Defense_EPA_Delta'].values

fig, ax = plt.subplots(figsize = (15, 15))
ax.grid(alpha=0.5)

ax.vlines(0, -0.2, 0.2, color='#fcc331', alpha=0.7, lw=4, linestyles='dashed')
ax.hlines(0, -0.2, 0.2, color='#fcc331', alpha=0.7, lw=4, linestyles='dashed')
ax.set_ylim(-0.1, 0.1)
ax.set_xlim(-0.1, 0.1)
ax.set_xlabel('Offense_EPA_Delta', fontsize=20)
ax.set_ylabel('Defense_EPA_Delta', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

annot_styles = {
    'bbox': {'boxstyle': 'round,pad=0.5', 'facecolor': 'none', 'edgecolor':'#fcc331'},
    'fontsize': 20,
    'color': '#202f52'
}

# annotate the axis
ax.annotate('Increasing Offense Difficulty', xy=(0.06,0), **annot_styles)
ax.annotate('Decreasing Offense Difficulty', xy=(-0.1,-0.015), **annot_styles)
ax.annotate('Decreasing Defense Difficulty', xy=(-0.03,0.08), **annot_styles)
ax.annotate('Increasing Defense Difficulty', xy=(-0.03,-0.085), **annot_styles)

team_colors = pd.read_csv('https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/teams_colors_logos.csv')

# annotate the points with team logos
for idx, row in schedule_epa.iterrows():
    offense_epa = row['Offense_EPA_Delta']
    defense_epa = row['Defense_EPA_Delta']
    logo_src = team_colors[team_colors['team_abbr'] == idx]['team_logo_espn'].values[0]
    res = requests.get(logo_src)
    img = plt.imread(BytesIO(res.content))
    ax.imshow(img, extent=[row['Offense_EPA_Delta']-0.0085, row['Offense_EPA_Delta']+0.0085, row['Defense_EPA_Delta']-0.00725, row['Defense_EPA_Delta']+0.00725], aspect='equal', zorder=1000)

ax.set_title('Offense EPA and Defense EPA', fontsize=20);
plt.show()