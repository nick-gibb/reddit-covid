# Scrape Reddit content on COVID-19

To run on Windows: 

1. Make a virtual env: `python -m venv venv`

2. Activate virtual env: `venv\Scripts\activate`

3. Install dependencies: `pip install -r requirements.txt`

4. Run the program: `python main.py`

To run on Docker: 

1. Build image: `docker build --tag redditscrape:latest .`

2. Run container: `docker run -it --rm --name redditdev --mount type=bind,source="$pwd)"/reddit_scrape,target=/code redditscrape hi hi`