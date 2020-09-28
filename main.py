from datetime import date, timedelta
from pprint import pprint
import json
import requests as r
import time


def make_date_range(sdate, edate):
    delta = edate - sdate
    timestamps = []

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        unix_timestamp = str(int(time.mktime(day.timetuple())))
        timestamps.append(unix_timestamp)
    return timestamps


def export_submissions(subreddits, queries, timestamps):

    file_export_name = "data2"

    for query in queries:
        print(f'Query: {query}')

        for subreddit in subreddits:
            print(f'Subreddit: {subreddit}')

            for i in range(len(timestamps)):
                
                try:
                    query = "covid"

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
                    
                    print("Data exported to {name}".format(name=file_export_name))

                except json.decoder.JSONDecodeError:
                    print("Failed to parse: {api_call}")
                    print("Adding url to an errors text file") 

                    with open(f"{file_export_name}_error_url.txt", 'a', encoding='utf-8') as error_file:
                        error_file.write("{api_call}\n")
                    
                    print("Done adding url to errors.txt file.  Continuing on...") 
                    continue


def main():
    #edate = date.today()
    sdate = date(2020, 4, 1)
    edate = date(2020, 4, 30)
    timestamps = make_date_range(sdate, edate)
    export_submissions(subreddits=['Canada', 'CanadaPolitics', 'CanadaCoronavirus', 'Vancouver', 'Edmonton', 'Winnipeg', 'Montreal', 'Ottawa', 'Saskatoon', 'Calgary', 'Toronto', 'Ontario'], queries=[
                                 'covid', 'coronavirus','sars-cov-2'], timestamps=timestamps)

if __name__ == "__main__":
    main()
