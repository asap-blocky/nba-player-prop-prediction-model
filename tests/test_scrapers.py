import unittest
from unittest.mock import Mock
from src.player_scraper import get_game_logs


class TestGetGameLogs(unittest.TestCase):

    def test_get_game_logs(self):
        player_name = "LeBron James"
        season_year = 2022

        mock_lookup = Mock(return_value="lebron james")
        mock_get_player_suffix = Mock(return_value="/players/j/jamesle01.html")

        expected_output = pd.DataFrame({
            "Date": ["2021-10-19", "2021-10-22"],
            "Opp": ["GSW", "POR"],
            "Result": ["L (-12)", "L (-8)"],
            "MP": ["37:28", "35:55"],
            "FG": ["9-21", "10-20"],
            "FG%": [".429", ".500"],
            "3P": ["1-6", "1-5"],
            "3P%": [".167", ".200"],
            "FT": ["3-3", "2-2"],
            "FT%": ["1.000", "1.000"],
            "ORB": ["2", "0"],
            "DRB": ["3", "3"],
            "TRB": ["5", "3"],
            "AST": ["7", "5"],
            "STL": ["0", "0"],
            "BLK": ["1", "0"],
            "TOV": ["2", "5"],
            "PF": ["3", "3"],
            "PTS": ["22", "23"],
            "+/-": ["-11", "-10"]
        })

        with patch("data.scrapers.lookup", mock_lookup):
            with patch("data.scrapers.get_player_suffix", mock_get_player_suffix):
                with patch("data.scrapers.requests.get") as mock_get:
                    mock_get.return_value.status_code = 200
                    mock_get.return_value.content = "<html><body><table id='pgl_basic'>...</table></body></html>"
                    mock_soup = Mock()
                    mock_find_all = Mock(return_value=["2021-10-19", "GSW", "L (-12)", "37:28", "9-21", ".429",
                                         "1-6", ".167", "3-3", "1.000", "2", "3", "5", "7", "0", "1", "2", "3", "22", "-11"])
                    mock_soup.find_all = mock_find_all
                    with patch("data.scrapers.BeautifulSoup", return_value=mock_soup):
                        actual_output = get_game_logs(player_name, season_year)

        pd.testing.assert_frame_equal(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
