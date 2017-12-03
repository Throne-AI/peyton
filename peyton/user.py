import datetime
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests

class User(object):

    def __init__(self, api):
        """
        Contains methods for retrieving user based data
        """
        self.api = api # Throne API instance with auth information

    def get_xp(self):
        """
        Retrieves User XP

        Returns
        --------
        int - the XP of the user
        """
        result = requests.get('%s%s' % (self.api.BASE_URL, 'user/xp/'), headers=self.api.headers)
        self.api._auth_report(result)

        return json.loads(result.content.decode("utf-8"))['result']['xp']

    def get_performance(self):
        """
        Retrieves User XP

        Returns
        --------
        dict - a dictionary of user performance data
        """
        result = requests.get('%s%s' % (self.api.BASE_URL, 'user/performance/'), headers=self.api.headers)
        self.api._auth_report(result)
        content = json.loads(result.content.decode("utf-8"))['result']

        self.competitions_entered = [name for name in content.keys() if name != 'total']
        self.score_dfs = {}

        # make dataframes for the historical scores for each competition
        for comp_key, comp_values in content.items():
            if comp_key == 'total':
                continue

            self.score_dfs[comp_key] = pd.DataFrame(content[comp_key]['score_series'])
            self.score_dfs[comp_key].columns = ['Throne Score']
            self.score_dfs[comp_key].index = [datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S') for date in content[comp_key]['score_dates']]

        self.edge_df = pd.DataFrame.from_dict({comp_key : comp_values['edge'] for comp_key, comp_values in content.items() if comp_key != 'total'}, orient='index')
        self.edge_df.columns = ['Edge']

        return content

    def plot_edge(self):
        """
        Plots the user edge for each competition

        Returns
        --------
        A plot of the user score for the competition
        """

        if not hasattr(self, 'edge_df'):
            self.get_performance()

        try:
            self.edge_df.plot.bar(rot=0); plt.axhline(0, color='k'); plt.title("Log Loss Difference: negative values are good"); plt.show()
        except AttributeError:
            raise AttributeError('You have no records in any competition')

    def plot_score(self, competition):
        """
        Plots the score for a given competition

        Parameters
        --------
        competition - str
            The name of the competition, e.g. "Spanish La Liga"

        Returns
        --------
        A plot of the user score for the competition
        """

        if not hasattr(self, 'score_dfs'):
            self.get_performance()

        try:
            self.score_dfs[competition].plot.area(); plt.show()
        except AttributeError:
            raise AttributeError('You have no records in any competition')
        except KeyError:
            raise KeyError('You have no record for a competition called %s. You are only entered in competitions: %s ' % (competition, self.competitions_entered))