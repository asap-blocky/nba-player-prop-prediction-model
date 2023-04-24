import requests
from bs4 import BeautifulSoup

# Function to scrape active players from a single page


def scrape_active_players(url):
    active_players = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    players_table = soup.find("table", {"id": "players"})

    for row in players_table.find("tbody").find_all("tr"):
        player_name = row.find("th", {"data-stat": "player"})
        # Active players have their names in bold/strong
        if player_name and player_name.find("strong"):
            active_players.append(player_name.get_text())

    return active_players


# Loop through the alphabet and collect active players' names
all_active_players = []
alphabet = "abcdefghijklmnopqrstuvwxyz"

for letter in alphabet:
    url = f"https://www.basketball-reference.com/players/{letter}/"
    active_players = scrape_active_players(url)
    all_active_players.extend(active_players)

# # Print the list of all active players, one per line
# print('\n'.join(all_active_players))
