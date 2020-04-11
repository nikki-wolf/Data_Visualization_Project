# Data_Visualization_Project
It is a hobby project for >1M records of gloabl wine history. It's based on a JavaScript code for the front-end and Python code for the backend connected through the Flask. This dashboard is laso implemented into Heroku (https://wine-history-price-rating.herokuapp.com/)

Collections in mongodb based mLab databases (connected to Heroku):
 1) wine_hist_onedoc : wine history by applying a JSON file including history for all countries and years (collection documents size: 1).
 2) wine_history: wine history by applying features per country per year (collection document size: 53 country * 152 years).
 3) wine_history_list: wine history by applying features per country for all years (collection document size: 53 country).
 4) wine_rating: wine price, rating, and variety features (collection document size: 120915)
 5) wine_rating_World: wine price, rating, and variety features per country for all countries worldwide including The US (collection document size: 42 producing countries)
 6) wine_rating_States: wine price, rating, and variety features per The States for The US (collection document size: 27 producing states).

Based on our performance benchmark, I used wine_history_list and (wine_rating_World + wine_rating_states) for the wine history and list features respectively.

