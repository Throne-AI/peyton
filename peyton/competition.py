import datetime
import io
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import zipfile

SUBMISSION_ROWS_TO_EXTRACT = ['id', 'team_1_prob', 'team_2_prob', 'team_tie_prob']


class UploadError(Exception):
    pass


class Competition(object):

    def __init__(self, api):
        """
        Contains methods for retrieving user based data
        """
        self.api = api # Throne API instance with auth information

    def __call__(self, competition_name):
        """
        When the user calls, we set the competition name
        """

        self.competition = competition_name
        self.api.headers['X-COMPETITION-NAME'] = self.competition

        return self

    def get_historical_data(self, file_dir=None):
        """
        Retrieves User XP

        Returns
        --------
        int - the XP of the user
        """

        if hasattr(self, 'historical_data'):
            return self.historical_data

        # user specified location
        if file_dir:
            self.historical_data = pd.read_csv(file_dir)
            return self.historical_data

        # If we reach this point, we're going through the API
        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/data/historical/'), headers=self.api.headers)
        self.api._auth_report(result)

        # extract csv form zip and read into pandas DataFrame
        zp = zipfile.ZipFile(io.BytesIO(result.content))

        file_names = [file.filename for file in zp.infolist() if '_historical_data' in file.filename]

        if not file_names:
            raise IndexError('No relevant data files detected')
        elif len(file_names) > 1:
            raise IndexError('More than one file detected - faulty endpoint')
        else:
            file_to_extract = file_names[0]

        self.historical_data = pd.read_csv(zp.open(file_to_extract))

        return self.historical_data

    def get_competition_data(self, file_dir=None):
        """
        Retrieves User XP

        Returns
        --------
        int - the XP of the user
        """

        if hasattr(self, 'competition_data'):
            return self.competition_data

        # user specified location
        if file_dir:
            self.competition_data = pd.read_csv(file_dir)
            return self.competition_data

        # If we reach this point, we're going through the API
        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/data/upcoming/'), headers=self.api.headers)
        self.api._auth_report(result)

        # extract csv form zip and read into pandas DataFrame
        zp = zipfile.ZipFile(io.BytesIO(result.content))

        file_names = [file.filename for file in zp.infolist() if '_competition_data' in file.filename]

        if not file_names:
            raise IndexError('No relevant data files detected')
        elif len(file_names) > 1:
            raise IndexError('More than one file detected - faulty endpoint')
        else:
            file_to_extract = file_names[0]

        self.competition_data = pd.read_csv(zp.open(file_to_extract))

        return self.competition_data

    def submit(self, df):
        """
        Submits predictions for upcoming games
        """
        try:
            if 'team_tie_prob' not in df.columns:
                final_df = df[['id', 'team_1_prob', 'team_2_prob']]
            else:
                final_df = df[SUBMISSION_ROWS_TO_EXTRACT]
        except KeyError:
            raise KeyError('Could not find probability (team_1_prob, team_2_prob) or ID columns (id) in your submitted DataFrame')
        
        self.api.headers['X-PROB-SUBMISSION'] = json.dumps(final_df.to_dict())

        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/submit/'), headers=self.api.headers)
        self.api._auth_report(result)

        content = json.loads(result.content.decode("utf-8"))['result']

        if not content['success']:
            raise UploadError(content['error'])
        else:
            return content