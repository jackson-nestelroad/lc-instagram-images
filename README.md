# Life.Church Instagram Image Web Server
This repository is a very small web server that returns the Instagram images for the current Life.Church sermon series.
The server scrapes the Life.Church and Open Network websites each day and updates a PostgreSQL database.

This web server was produced over two coding sessions.

**Version 1**
- Flask server that scrapes for the images on each request.
- Images presented in simple HTML.

**Version 2**
- Web scraping was moved to a background script run once a day.
- Image links are stored in a PostgreSQL database and retrieved on GET requests.
