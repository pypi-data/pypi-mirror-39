import os
import time

import requests

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
PROCESSING = 'PROCESSING'
ERROR = 'ERROR'


class MessagesMixin:

    @property
    def upload_successful(self):
        return '\nFile uploaded successfully'

    @property
    def retry_msg(self):
        return (
            'You submission is being evaluated.'
            '\n\tNote:If your submission is in evaluation status for'
            ' more than 30 min please contact support with submission'
            ' id, on a PRIVATE chat.\n\tPLEASE DO NOT SHARE YOUR API'
            ' KEY ON A PUBLIC THREAD')

    @property
    def error_msg(self):
        return (
            'Oops something went wrong during transgalactic transmission.'
            'Are you sure about the submission id?')

    @property
    def max_submission(self):
        return (
            'You have exceeded maximum allowed submissions'
            '\nPlease proceed with marking your final submission')


class Result(MessagesMixin):

    def __init__(self, json):
        self._json = json
        self._keys = set()
        self.submission_id = None
        self.status = None
        self.message = None
        self.score = None
        self._setattr()

    def __call__(self, json):
        self._json = json
        self._setattr()

    def _setattr(self):
        self._clear()
        for k, v in self._json.items():
            setattr(self, k, v)
            self._keys.add(k)

    def _clear(self):
        for key in self._keys:
            delattr(self, key)
        self._keys = set()

    def print_upload_msg(self):
        text = ('\tYou submission id is {}'
                '\n\tPlease take a note of the submission id for'
                ' finalizing your submission.')
        print(self.upload_successful)
        print(text.format(self.submission_id))

    def print_result_msg(self):
        text = '\tThe submission accuracy is {}'.format(self.score)
        print(text)

    def print_result_failure_msg(self):
        text = '\tThe submission accuracy is {}'.format(self.score)
        print(text)

    def print_timeout_msg(self):
        text = ('Evaluation is taking longer that usual.'
                '\nPlease wait for 10 minutes and try: '
                '\n\t\tmlr.result({})'.format(self.submission_id))
        print(text)

    def print_list_submissions(self):
        print('Your submissions are:')
        for submission_id, score in self.result.items():
            print('\t{}\t\t{}'.format(submission_id, score))

    def print_finalize_submission(self):
        text = ('Submission ({}) with a score of {}'.format(
            self.submission_id, self.score) +
                ' is marked for final evaluation')
        print(text)

    @staticmethod
    def handle_401(other_self):
        text = (
            'Request Unauthorized!'
            '\nPlease verify your api key and employee id.'
            '''Employee id:{0.participant_id}
            API Key{0.api_key}'''.format(other_self))
        print(text)

    @staticmethod
    def handle_429():
        text = (
            '\tYou have exceeded maximum allowed request.'
            '\n\tPlease proceed with finalizing your submission')
        print(text)

    def handle_500(self, action):
        text = 'An error occurred during {}'.format(action)
        if action == 'uploading file':
            text += '\tHint: Please check the file format.'
        print(text)


class MLRank:
    """
    import mlrank
    mlr = mlrank('participant_id', 'your_api_key')
    mlr.score('file_path/file.csv')
    mlr.submit('submission_id')
    """
    __version__ = '0.0.1a1.post1'

    def __init__(self, participant_id: int, api_key: str,
                 service_description_uri: str = None, **kwargs):
        self.participant_id = participant_id
        self.api_key = api_key
        self._base_url = self._get_remote_service(
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

    def _network_issue(self, status_code, action):
        if status_code == 401:
            Result.handle_401(self)
        elif status_code == 429:
            Result.handle_429()
        elif status_code == 500:
            Result.handle_500()
        else:
            raise ConnectionError(
                'An error occurred while {}'
                ': status code {}'.format(action, status_code))

    def _file_upload(self, file: str) -> Result:
        if not os.path.isfile(file):
            raise FileNotFoundError('{} does not exist.'.format(file))
        if not isinstance(self.participant_id, int):
            raise ValueError('{0.participant_id} is not  valid,'.format(self) +
                             ' pass an integer value.')
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/octet-stream',
        }

        with open(file, 'rb') as data:
            url = '{0._base_url}/upload/{0.participant_id}/data.csv'.format(self)
            response = requests.put(url, data=data, headers=headers)
            if response.ok:
                return Result(response.json())
            self._network_issue(response.status_code, 'uploading file')

    def _get_score(self, submission_id: str) -> Result:
        headers = {
            'x-api-key': self.api_key,
        }
        url = '{}/result/{}/{}'.format(
            self._base_url, self.participant_id, submission_id)
        response = requests.get(url, headers=headers)
        if response.ok:
            return Result(response.json())
        self._network_issue(response.status_code, 'retrieving result')

    def _await_eval(self, retry: bool = False):
        waiting = '\nWaiting for evaluation'
        retrying = '\nEvaluation pending'
        print(retrying if retry else waiting,
              end='', flush=True)
        for _ in range(self._wait_sec):
            time.sleep(1)
            print('.', end='', flush=True)
        print()

    @staticmethod
    def _print_result(result: Result):
        if result.status == SUCCESS:
            result.print_result_msg()
        elif result.status == PROCESSING:
            print(result.retry_msg)
        elif result.status == ERROR:
            print(result.error_msg)

    def result(self, submission_id: str):
        result = self._get_score(submission_id)
        if result:
            self._print_result(result)

    def submit(self, file: str) -> None:
        print('Preparing to upload file...')
        result = self._file_upload(file)
        if result:
            result.print_upload_msg()
            self._await_eval()
            print('\nRetrieving result...')
            result = self._get_score(result.submission_id)
            if result:
                for _ in range(3):
                    if result is None or result.status != PROCESSING:
                        break
                    self._await_eval(retry=True)
                    result = self._get_score(result.submission_id)
                else:
                    result.print_timeout_msg()
                    return
                if result:
                    self._print_result(result)

    def _list_submissions(self) -> Result:
        headers = {
            'x-api-key': self.api_key,
        }
        url = '{}/list/{}'.format(self._base_url, self.participant_id)
        response = requests.get(url, headers=headers)
        if response.ok:
            return Result(response.json())
        self._network_issue(response.status_code, 'listing submission')

    def list_submissions(self):
        result = self._list_submissions()
        if result:
            result.print_list_submissions()

    def _mark_submission(self, submission_id):
        headers = {
            'x-api-key': self.api_key,
        }
        url = '{}/submit/{}/{}'.format(
            self._base_url, self.participant_id, submission_id)
        response = requests.post(url, headers=headers)
        if response.ok:
            return Result(response.json())
        self._network_issue(response.status_code, 'finalizing submission')

    def mark_final(self, submission_id):
        result = self._mark_submission(submission_id)
        if result:
            result.print_finalize_submission()
