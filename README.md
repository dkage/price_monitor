# Price Monitor

Simple project for analyzing prices for PC parts I'm wanting to buy, made in Flask and Jinja2 with BeautifulSoup,
as a learning project to better understand how to show Python data using Jinja syntax. 

Basically it works by using web scrapers to check the prices of the registered products many times a day, and storing those prices in a PostgreSQL database. By storing the data that way it is possible to check not only the best current price, but the best price that product has ever been since the project is running.
