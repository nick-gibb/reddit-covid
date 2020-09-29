from datetime import date, timedelta
import datetime
from pprint import pprint
import json
import requests as r
import time


def make_date_range(start_date:datetime.timedelta, end_date: datetime.timedelta) -> datetime.timedelta:
    delta = end_date - start_date
    timestamps = []

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        unix_timestamp = str(int(time.mktime(day.timetuple())))
        timestamps.append(unix_timestamp)

    return timestamps


def export_submissions(subreddit:str, query:str, timestamps:datetime.timedelta, num_retries:int=1, file_export_name:str="data") -> None:

    for i in range(len(timestamps)):
        
        for num_retry in range(num_retries+1):

            try:

                if i == len(timestamps)-1:
                    break

                after = timestamps[i]
                before = timestamps[i+1]
                api_call = f'https://api.pushshift.io/reddit/search/submission/?q={query}&subreddit={subreddit}&after={after}&before={before}&limit=500'
                
                time.sleep(1.2)

                req = r.get(api_call)

                submission = req.json()['data'] 

                with open(f"{file_export_name}.json", 'a', encoding='utf-8') as f:
                    json.dump(submission, f, ensure_ascii=False, indent=4)
                
                print(f"Data exported to {file_export_name}.csv")

            except json.decoder.JSONDecodeError:
                print(f"Failed to parse: {api_call}")
                print(f"Adding url to {file_export_name}_errors.txt file") 

                with open(f"{file_export_name}_error_url.txt", 'a', encoding='utf-8') as error_file:
                    error_file.write("{api_call}\n")
                
                print(f"Done adding url to {file_export_name}_errors.txt file.  Continuing on...") 
                continue 

            break


def main() -> None:
    #edate = date.today()
    start_date = date(2020, 4, 1)
    end_date = date(2020, 4, 30)
    timestamps = make_date_range(start_date, end_date)
    
    queries=['covid', 'coronavirus','sars-cov-2']
    subreddits=['Canada', 'CanadaPolitics', 'CanadaCoronavirus', 
                'Vancouver', 'Edmonton', 'Winnipeg', 
                'Montreal', 'Ottawa', 'Saskatoon', 
                'Calgary', 'Toronto', 'Ontario', "onguardforthee"]

    for query in queries:
        print(f'Query: {query}')

        for subreddit in subreddits:
            print(f'Subreddit: {subreddit}')

            export_submissions(subreddit=subreddit, query=query, timestamps=timestamps)

if __name__ == "__main__":
    main()
