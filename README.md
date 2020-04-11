# Data_Visualization_Project
It is a hobby project for >1M records of global wine history. It's based on a JavaScript code for the front-end and Python code for the backend connected through the Flask. This dashboard is also implemented into a Platform-as-a-service aka Heroku (https://wine-history-price-rating.herokuapp.com/).

Note: The performance of the app response is degraded in the Heroku due to the dyno type that is selected currently. If a Performance-M/L dyno is selected, it dedicates 14 GB of RAM to render data as compared to that of current standard free dyno (i.e., only 0.5 GB of RAM).

The dashboard includes a map followed by three charts:
1) A global map visualizing the wine history per country for four productions. Upon clicking on each country with available wine data, a dynamic line chart shows the time-series of wine production, consumption, import, and export for 1861-2016. Also, by clicking on toggling on the right upper corner of the map, the user can select among wine production/consumption/export/import to see the qualitative circles for a specified year as selected by the scroller below the map. The size of circles shows the rank of the selected property for each country on a global scale (i.e., the larger the circle size, the higher the value fo that property for the shown country).

2) A dynamic bubble chart depicting the consumption per capita vs. production per capita on a global scale. The radius of each circle (country) is proportional to the excess volume per capita (i.e. production + import - consumption - export). The circle colors represent each country. By changing the expected year for reporting (the scroll bar above the bubble chart), the bubble chart is dynamically updated.

3) A hierarchy of wine types per country for all wine-producing countries. Click on the circle next to the name of each country to see what major type of wines that the country produces. At the next level, click on any of the major types, to show the producing wine sub-categories.

4) 

Collections in MongoDB based mLab databases (connected to Heroku):
 1) wine_hist_onedoc: wine history by applying a JSON file including history for all countries and years (collection documents size: 1).
 2) wine_history: wine history by applying features per country per year (collection document size: 53 countries * 152 years).
 3) wine_history_list: wine history by applying features per country for all years (collection document size: 53 countries).
 4) wine_rating: wine price, rating, and variety features (collection document size: 120915)
 5) wine_rating_World: wine price, rating, and variety features per country for all countries worldwide including The US (collection document size: 42 producing countries)
 6) wine_rating_States: wine price, rating, and variety features per The States for The US (collection document size: 27 producing states).

Based on our performance benchmark, I used wine_history_list and (wine_rating_World + wine_rating_states) for the wine history and list features respectively.
