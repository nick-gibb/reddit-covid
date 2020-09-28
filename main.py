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


def get_submissions(subreddits, queries, timestamps):

    submissions = []
    for query in queries:
        print(f'Query: {query}')
        for subreddit in subreddits:
            total_comments = 0
            print(f'Subreddit: {subreddit}')
            submission_count = 0
            for i in range(len(timestamps)):
                query = "covid"
                if i == len(timestamps)-1:
                    break
                after = timestamps[i]
                before = timestamps[i+1]
                api_call = f'https://api.pushshift.io/reddit/search/submission/?q={query}&subreddit={subreddit}&after={after}&before={before}&limit=500'
                # time.sleep(1)
                req = r.get(api_call)

                if 'json' in req.headers.get('Content-Type'):
                    resp = req.json()['data']
                    submission_count += len(resp)
                else:
                    pprint(api_call)
                    pprint(req.headers.get('Content-Type'))

                    pprint(req.json())
                    breakpoint
                    # print('Response content is not in JSON format.')
                    continue
                for submission in resp:
                    total_comments += submission['num_comments']
                    # reduced_submission = {
                    #     'full_link': submission['full_link'],
                    #     'title': submission['title'],
                    #     'num_comments': submission['num_comments'],
                    #     'score': submission['score'],
                    #     'created_utc': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(submission['created_utc']))
                    # }
                    submissions.append(submission)
            print(
                f'Post submission count in /r/{subreddit} with query "{query}": {submission_count}')
            print(
                f'Comment count in /r/{subreddit} with query "{query}": {total_comments}')
    return submissions


def main():
    sdate = date(2020, 4, 1)
    # edate = date(2020, 9, 3)
    edate = date.today()
    timestamps = make_date_range(sdate, edate)
    submissions = get_submissions(subreddits=['Canada', 'CanadaPolitics', 'CanadaCoronavirus', 'Vancouver', 'Edmonton', 'Winnipeg', 'Montreal', 'Ottawa', 'Saskatoon', 'Calgary', 'Toronto', 'Ontario'], queries=[
                                  'covid', 'coronavirus'], timestamps=timestamps)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(submissions, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
