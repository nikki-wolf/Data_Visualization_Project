# Data_Visualization_Project
Project2

Collections in mLab db (connected to Heroku):
 1) wine_hist_onedoc : wine history by applying a JSON file including history for all countries and years (collection documents size: 1).
 2) wine_history: wine history by applying features per country per year (collection document size: 53 country * 152 years).
 3) wine_history_list: wine history by applying features per country for all years (collection document size: 53 country).
 4) wine_rating: wine price, rating, and variety features (collection document size: 120915)
 5) wine_rating_World: wine price, rating, and variety features per country for all countries worldwide including The US (collection document size: 42 producing countries)
 6) wine_rating_States: wine price, rating, and variety features per The States for The US (collection document size: 27 producing states).

Based on our performance benchmark, we used wine_history_list and (wine_rating_World + wine_rating_states) for the wine history and list features respectively.

