import argparse
from datetime import date, timedelta
import datetime
import json
import logging
import requests as r
import sys
import time
from typing import List, Dict
from export_to_json import build_json_file, build_error_text_file


parser = argparse.ArgumentParser(
    description="Get start and end dates."
)
parser.add_argument("--sdate", required=True)
parser.add_argument("--edate")


logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


def make_date_range(sdate: datetime.timedelta, edate: datetime.timedelta) -> datetime.timedelta:
    delta = edate - sdate
    timestamps = []

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        unix_timestamp = str(int(time.mktime(day.timetuple())))
        timestamps.append(unix_timestamp)

    return timestamps


def export_submissions(subreddit: str, query: str, timestamps: datetime.timedelta, num_retries: int = 1, file_export_name: str = "data2") -> List[str]:
    '''
    Exports query as a JSON object and retrieves a list of ids for further processing

    Return:
        List[str]

        All the IDs retrieved by the API
    '''

    for i, timestamp in enumerate(timestamps[:-1]):

        for num_retry in range(num_retries+1):

            try:

                after = timestamp
                before = timestamps[i+1]
                api_call = f'https://api.pushshift.io/reddit/search/submission/?q={query}&subreddit={subreddit}&after={after}&before={before}&limit=500'

                time.sleep(2)

                req = r.get(api_call)

                submission = req.json()['data']

                build_json_file(submission, file_export_name)

                logging.info(f"Data exported to {file_export_name}.csv")

            except json.decoder.JSONDecodeError:
                logging.info(f"Failed to parse: {api_call}")
                logging.info(f"Adding to an error.txt file")

                build_error_text_file(f"api_call\n", file_export_name)

                logging.info(
                    f"Done adding url to {file_export_name}_errors.txt file.  Continuing on...")
                continue

            break

        return [data['id'] for data in submission]


def get_comments_id_from_submission_id(submission_id: str, num_retries: int = 1, file_export_name="data_comment_and_sub_ids2") -> List[str]:
    '''
    Given the ids generated by the submission endpoint, their corresponding 
    comment ids are generated. 

    Return:
        List[Dict[str,str]] 

        A list of dictionaries containing the comment id and the submission id
    '''
    list_comments_submission_id = list()

    for num_retry in range(num_retries+1):

        try:

            comment_ids = f"https://api.pushshift.io/reddit/submission/comment_ids/{submission_id}"
            comment_ids = r.get(comment_ids).json()["data"]

            time.sleep(2)

            for id in comment_ids:
                list_comments_submission_id.append(
                    {"submission_id": submission_id, "comment_id": id})

            build_json_file(list_comments_submission_id, file_export_name)

            logging.info(f"Data exported to {file_export_name}.csv")

        except json.decoder.JSONDecodeError:
            logging.info(f"Failed to parse comments_submission_ids bridge")
            logging.info(f"Adding to an error.txt file")

            build_error_text_file(f"{comment_ids}\n", file_export_name)

            logging.info(
                f"Done adding url to {file_export_name}_bridge_errors.txt file.  Continuing on...")

            continue

        break

    return[item["comment_id"] for item in list_comments_submission_id]


def get_comments(comment_ids: List[str], num_retries: int = 1, file_export_name: str = "comments_data2") -> None:

    comment_string = ','.join(comment_ids)

    for num_retry in range(num_retries+1):

        try:

            api_call = f'https://api.pushshift.io/reddit/search/comment?ids={comment_string}'

            time.sleep(2)

            req = r.get(api_call)

            comments = req.json()['data']

            build_json_file(comments, file_export_name)

            logging.info(f"Data exported to {file_export_name}.csv")

        except json.decoder.JSONDecodeError:
            logging.info(f"Failed to parse: {api_call}")
            logging.info(f"Adding url to {file_export_name}_errors.txt file")

            build_error_text_file(f"{api_call}\n", file_export_name)

            logging.info(
                f"Done adding url to {file_export_name}_errors.txt file.  Continuing on...")
            continue

        break


def main(sdate, edate) -> None:

    timestamps = make_date_range(sdate, edate)

    queries = ['covid', 'coronavirus', 'sars-cov-2']
    subreddits = ['Canada', 'CanadaPolitics', 'CanadaCoronavirus',
                  'Vancouver', 'Edmonton', 'Winnipeg',
                  'Montreal', 'Ottawa', 'Saskatoon',
                  "Saskatchewan", "Alberta", "Quebec", "NovaScotia",
                  "NewBrunswickCanada", "Newfoundland", "Manitoba",
                  "BritishColumbia",
                  'Calgary', 'Toronto', 'Ontario', "onguardforthee"]

    for query in queries:
        for subreddit in subreddits:
            logging.info(f'Retrieving posts with \'{query}\' in /r/{subreddit}')

            posts_id = export_submissions(subreddit, query, timestamps)

            for post_id in posts_id:
                comments_id = get_comments_id_from_submission_id(post_id)

                get_comments(comments_id)


if __name__ == "__main__":
    args = parser.parse_args()

    sdate = datetime.datetime.strptime(args.sdate, '%Y-%m-%d').date()

    if args.edate:
        edate = datetime.datetime.strptime(args.edate, '%Y-%m-%d').date()
    else:
        edate = date.today()

    main(sdate, edate)
