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


class AvailabilityError(Exception):
    pass


class Competition(object):

    def __init__(self, api):
        """
        Contains methods for retrieving competition based data
        """
        self.api = api # Throne API instance with auth information

    def __call__(self, competition_name):
        """
        When the user calls, we set the competition name
        """

        if hasattr(self, 'competition'):
            if self.competition != competition_name:
                try:
                    del self.historical_data
                except AttributeError:  # historical data has not been fetched
                    pass
                try:
                    del self.competition_data
                except AttributeError:  # competition data has not been fetched
                    pass
                try:
                    del self.game_statistics_data
                except AttributeError:  # game statistics data has not been fetched
                    pass
                try:
                    del self.lineups_data
                except AttributeError:  # lineups data has not been fetched
                    pass
                try:
                    del self.players_data
                except AttributeError:  # players data has not been fetched
                    pass

        self.competition = competition_name
        self.api.headers['X-COMPETITION-NAME'] = self.competition

        return self

    @property
    def available(self):
        """
        Find available competitions
lflflf
        Returns
        --------
        - list of available competitions (name strs that you can query)
        """

        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/data/names/'), headers=self.api.headers)
        self.api._auth_report(result)

        return json.loads(result.content.decode("utf-8"))['result']

    def get_historical_data(self, file_dir=None):
        """
        Retrieves and sets historical data for the competition.

        Returns
        --------
        self.historical_data - the competition's historical data
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

    def get_game_statistics_data(self, file_dir=None):
        """
        Retrieves and sets game statistics data for the competition.

        Returns
        --------
        self.game_statistics_data - the competition's game statistics data
        """

        if hasattr(self, 'game_statistics_data'):
            return self.game_statistics_data

        # user specified location
        if file_dir:
            self.game_statistics_data = pd.read_csv(file_dir)
            return self.game_statistics_data

        # If we reach this point, we're going through the API
        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/data/gamestatistics/'), headers=self.api.headers)
        self.api._auth_report(result)

        # extract csv form zip and read into pandas DataFrame
        try:
            zp = zipfile.ZipFile(io.BytesIO(result.content))
        except zipfile.BadZipFile:
            error_message = json.loads(str(result.content.decode('utf-8')))
            raise AvailabilityError(error_message['message'])

        file_names = [file.filename for file in zp.infolist() if '_game_statistics_data' in file.filename]

        if not file_names:
            raise IndexError('No relevant data files detected')
        elif len(file_names) > 1:
            raise IndexError('More than one file detected - faulty endpoint')
        else:
            file_to_extract = file_names[0]

        self.game_statistics_data = pd.read_csv(zp.open(file_to_extract))

        return self.game_statistics_data

    def get_lineups_data(self, file_dir=None):
        """
        Retrieves and sets lineups data for the competition.

        Returns
        --------
        self.lineups_data - the competition's lineups data
        """

        if hasattr(self, 'lineups_data'):
            return self.lineups_data

        # user specified location
        if file_dir:
            self.lineups_data = pd.read_csv(file_dir)
            return self.lineups_data

        # If we reach this point, we're going through the API
        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/data/lineups/'), headers=self.api.headers)
        self.api._auth_report(result)

        # extract csv form zip and read into pandas DataFrame
        try:
            zp = zipfile.ZipFile(io.BytesIO(result.content))
        except zipfile.BadZipFile:
            error_message = json.loads(str(result.content.decode('utf-8')))
            raise AvailabilityError(error_message['message'])

        file_names = [file.filename for file in zp.infolist() if '_lineups_data' in file.filename]

        if not file_names:
            raise IndexError('No relevant data files detected')
        elif len(file_names) > 1:
            raise IndexError('More than one file detected - faulty endpoint')
        else:
            file_to_extract = file_names[0]

        self.lineups_data = pd.read_csv(zp.open(file_to_extract))

        return self.lineups_data

    def get_players_data(self):
        """
        Retrieves player data for the competition

        Returns
        --------
        self.players_data - the players data for the competition
        """

        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/data/players/'), headers=self.api.headers)
        self.api._auth_report(result)

        self.players_data = json.loads(result.content.decode("utf-8"))['result']

        return self.players_data

    def get_competition_data(self, file_dir=None):
        """
        Retrieves and sets upcoming data for the competition.

        Returns
        --------
        self.competition_data - the competition's historical data
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
            if 'confidence' in df.columns:
                if 'team_tie_prob' not in df.columns:
                    final_df = df[['id', 'team_1_prob', 'team_2_prob', 'confidence']]
                else:
                    final_df = df[SUBMISSION_ROWS_TO_EXTRACT + ['confidence']]
            else:
                if 'team_tie_prob' not in df.columns:
                    final_df = df[['id', 'team_1_prob', 'team_2_prob']]
                else:
                    final_df = df[SUBMISSION_ROWS_TO_EXTRACT]

        except KeyError:
            raise KeyError('Could not find probability (team_1_prob, team_2_prob) or ID columns (id) in your submitted DataFrame')

        final_df.index = [str(i) for i in final_df.index] # str format because of json parsing differences

        self.api.headers['X-PROB-SUBMISSION'] = json.dumps(final_df.to_dict())

        result = requests.get('%s%s' % (self.api.BASE_URL, 'competition/submit/'), headers=self.api.headers)
        self.api._auth_report(result)

        content = json.loads(result.content.decode("utf-8"))['result']

        if not content['success']:
            raise UploadError(content['error'])
        else:
            return content
