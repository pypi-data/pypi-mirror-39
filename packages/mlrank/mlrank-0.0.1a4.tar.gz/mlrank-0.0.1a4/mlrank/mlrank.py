import os
import time

import requests

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
PROCESSING = 'PROCESSING'


class MLRank:
    """
    import mlrank
    mlr = mlrank('participant_id', 'your_api_key')
    mlr.score('file_path/file.csv')
    mlr.submit('submission_id')
    """

    SUBMISSIONS = dict()

    def __init__(self, participant_id: int, api_key: str,
                 service_description_uri: str = None, **kwargs):
        self.participant_id = participant_id
        self.api_key = api_key
        self.base_url = self._get_remote_service(
            service_description_uri)
        self._wait_sec = kwargs.get('wait', 5)

    @staticmethod
    def _get_remote_service(uri: str) -> dict:
        url = uri if uri else os.environ.get('SERVICE_DESCRIPTION_URI')
        if url is None:
            raise ValueError('Please provide evaluation service uri.')
        response = requests.get(url)
        if response.ok:
            return response.json().get('uri')
        return dict()

    def _file_upload(self, file: str) -> dict:
        if not os.path.isfile(file):
            raise FileNotFoundError('{} does not exist.'.format(file))
        if not isinstance(self.participant_id, int):
            raise ValueError('{0.participant_id} is not  valid,'.format(self) +
                             ' pass an integer value.')
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/octet-stream',
        }
        data = open(file, 'rb')
        url = '{0.base_url}/upload/{0.participant_id}/data.csv'.format(self)
        response = requests.put(url, data=data, headers=headers)
        print(response.status_code)
        if response.ok:
            return response.json()
        if response.status_code == 404:
            raise ConnectionError('An error occurred while uploading file'
                                  ': status code {0.status_code}'.format(response))
        return dict()

    def _get_score(self, submission_id: str):
        headers = {
            'x-api-key': self.api_key,
        }
        url = '{}/result/{}/{}'.format(
            self.base_url, self.participant_id, submission_id)
        response = requests.get(url, headers=headers)
        if not response.ok:
            raise ConnectionError('An error occurred while retrieving result'
                                  ': status code {}'.format(response.status_code))
        return response.json().get("message")

    def _await_eval(self, retry: bool = False):
        waiting = 'Waiting for evaluation'
        retrying = 'Evaluation pending'
        print(retrying if retry else waiting,
              end='', flush=True)
        for _ in range(self._wait_sec):
            time.sleep(1)
            print('.', end='', flush=True)
        print()

    @staticmethod
    def _print_result(result: str):
        if result in [SUCCESS, FAILURE]:
            print('You submission is evaluated to {}'.format(result))
        else:
            print('You submission is being evaluated.'
                  '\nNote:If your submission is in evaluation status for'
                  ' more than 30 min please contact support with submission'
                  ' id, on a PRIVATE chat.'
                  'PLEASE DO NOT SHARE YOUR API KEY ON A PUBLIC THREAD')

    def result(self, submission_id: str):
        result = self._get_score(submission_id)
        if result != PROCESSING:
            pass
        else:
            print('Submission is being evaluated.')

    def score(self, file: str) -> None:
        print('Preparing to upload file...')
        response = self._file_upload(file)
        message = response.get('message')
        submission_id = response.get('submission_id')
        print('File uploaded successfully.'
              '\t{}\nYou submission id is {}'.format(message,
                                                     submission_id) +
              '\t\nPlease take a note of the submission id for'
              ' finalizing your submission.')
        self._await_eval()
        print('Retrieving result...')
        result = self._get_score(submission_id)
        for _ in range(3):
            if result != PROCESSING:
                break
            self._await_eval(retry=True)
            result = self._get_score(submission_id)
        else:
            print('Evaluation is taking longer that usual.'
                  '\nPlease wait for 10 minutes and try: '
                  '\n\tmlrank.result({})'.format(submission_id))
        self._print_result(result)

    def _mark_submission(self, submission_id):
        pass

    def submit(self, submission_id):
        pass
