import requests
import pandas as pd
from bs4 import BeautifulSoup

from contraints import TEAM_TO_TEAM_ABBR
from requests_html import HTMLSession


def get_team_stats(team, season_end_year, data_format='PER_GAME'):
    url = f'https://www.basketball-reference.com/leagues/NBA_{season_end_year}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find both tables
    east_table = soup.find("table", {"id": "confs_standings_E"})
    west_table = soup.find("table", {"id": "confs_standings_W"})

    # Search both tables for the team's data
    for table in [east_table, west_table]:
        table_data = table.tbody.find_all("tr")
        data = []
        for row in table_data:
            team_name = row.find("th").get_text(strip=True)
            team_data = [td.get_text(strip=True) for td in row.find_all("td")]
            if team_data:
                data.append([team_name] + team_data)

        columns = ["Team"] + [th.get_text(strip=True)
                              for th in table.thead.tr.find_all("th")]
        # Remove the first column (rank), as it's not needed
        columns = columns[:1] + columns[2:]

        df = pd.DataFrame(data, columns=columns)
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df.loc[:, 'SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        s = df[df['TEAM'] == team]

        # If the team is found, return its stats
        if not s.empty:
            return pd.Series(index=list(s.columns), data=s.values.tolist()[0])


def get_team_misc(team, season_end_year):
    url = f'https://www.basketball-reference.com/teams/{team}/{season_end_year}.html'
    print(f'Fetching data from: {url}')

    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1)

    soup = BeautifulSoup(r.html.html, 'lxml')
    table = soup.find('table', {'id': 'team_misc'})

    if table:
        print("Table found!")

        # Read the table into a DataFrame
        dfs = pd.read_html(str(table), header=[0, 1])
        df = pd.concat(dfs, axis=1)

        # Remove multi-level column headers
        df.columns = df.columns.get_level_values(1)

        # Reset index
        df.reset_index(drop=True, inplace=True)

        # Rename columns
        new_column_names = ['Team', 'W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr',
                            'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'Opp eFG%', 'Opp TOV%', 'Opp DRB%', 'Opp FT/FGA', 'Arena', 'Attendance']
        df.columns = new_column_names

        # Add the row with league rank back into the DataFrame
        lg_rank = df[df['Team'] == 'Lg Rank']
    if not lg_rank.empty:
        df = pd.concat([df[df['Team'] != 'Lg Rank'], lg_rank], axis=0)

        # Remove numbers at the start of each row
        df['Team'] = df['Team'].str.replace(r'^\d+\s+', '')

        print("Data Frame created:")
        print(df)
    else:
        print("Table not found!")
