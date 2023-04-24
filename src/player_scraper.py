from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

from lookup import lookup
from get_player_suffix import get_player_suffix


def get_game_logs(player_name, season_year):
    player_name = lookup(player_name)
    player_suffix = get_player_suffix(player_name)
    if player_suffix is None:
        return None
    url = f"https://www.basketball-reference.com{player_suffix}/gamelog/{season_year}/"
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("table", {"id": "pgl_basic"})
    table_data = table.tbody.find_all("tr")

    data = []
    for row in table_data:
        game_data = [td.get_text(strip=True) for td in row.find_all("td")]
        if game_data:
            data.append(game_data)

    columns = [th.get_text(strip=True)
               for th in table.thead.find_all("th")][1:]
    df = pd.DataFrame(data, columns=columns)

    # Save the DataFrame to a CSV file
    df.to_csv('game_logs.csv', index=False)

    return df


def get_head_to_head_stats(player1, player2, season_year):
    player1_logs = get_game_logs(player1, season_year)
    player2_logs = get_game_logs(player2, season_year)

    # Filter game logs based on the opponent (i.e., the team the other player is playing for)
    player1_filtered = player1_logs[player1_logs['Opp']
                                    == player2_logs['Tm'].iloc[0]]
    player2_filtered = player2_logs[player2_logs['Opp']
                                    == player1_logs['Tm'].iloc[0]]

    # Merge the filtered game logs based on the game date
    head_to_head_stats = pd.merge(
        player1_filtered, player2_filtered, on='Date', suffixes=(f'_{player1}', f'_{player2}'))

    return head_to_head_stats


def get_advanced_player_stats(player_name, date):
    player_name = lookup(player_name)
    player_suffix = get_player_suffix(player_name)
    if player_suffix is None:
        return None
    url = f"https://www.basketball-reference.com{player_suffix}.html#all_advanced"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("table", {"id": "advanced"})
    table_data = table.tbody.find_all("tr")

    for row in table_data:
        game_date = row.get('id')
        if game_date == f"advanced.{date}":
            game_data = [td.get_text(strip=True) for td in row.find_all("td")]
            columns = [th.get_text(strip=True)
                       for th in table.thead.find_all("th")][1:]
            df = pd.DataFrame([game_data], columns=columns)
            return df

    print("Row not found")
    return None


def get_injuries():
    url = "https://www.basketball-reference.com/friv/injuries.cgi#site_menu_link"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("table", {"id": "injuries"})

    if table is None:
        print("Injuries table not found")
        return None

    table_data = table.tbody.find_all("tr", recursive=False)

    data = []
    for row in table_data:
        # new line to fetch player name
        player = row.find("th").get_text(strip=True)
        team = row.find_all("td")[0].get_text()
        update = row.find_all("td")[1].get_text()
        description = row.find_all("td")[2].get_text()

        expected_return = None
        match = re.search(r"\w{3}, \w{3} \d{1,2}, \d{4}", description)
        if match:
            expected_return = match.group()

        # include player in the data list
        data.append([player, team, update, description, expected_return])

    columns = ["Player", "Team", "Update", "Description",
               "Expected Return"]  # add "Player" to the columns list
    df = pd.DataFrame(data, columns=columns)

    return df


player = 'LeBron James'
year = 2022
logs = get_game_logs(player,  year)
print(logs)
