NBA Player Prediction Model Scraper
===================================

This project contains a set of Python scripts to scrape NBA player and team data from basketball-reference.com, which can be used to build a player performance prediction model.

Dependencies
------------

- requests
- pandas
- beautifulsoup4
- requests-html

Installation
------------

To install the required dependencies, run the following command:

.. code:: bash

    pip install -r requirements.txt

Usage
-----

To collect data for a specific player and season, run the following command:

.. code:: bash

    python src/main.py --player "Player Name" --season_end_year YYYY

Replace "Player Name" with the full name of the player and YYYY with the season's end year.

# nba-player-prop-prediction-model
