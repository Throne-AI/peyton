<img src="https://www.throne.ai/static/logos/logo-only-left-white.png" alt="Throne.AI" height=50 />

Peyton: Throne.ai API
===================================

**Peyton** is a Python library that allows you to interact with the <a href="https://www.throne.ai">Throne.ai</a> platform for sports prediction. From this library, you can download historical and competition data, user ranking data, and submit predictions.

Installation
------------

Peyton is developed for Python 3.5 onwards. The recommended way to
install peyton is via <a href="https://pypi.python.org/pypi/pip">pip</a>.

```
   pip install peyton
```

The <a href="http://docs.python-guide.org/en/latest/starting/installation">Hitchhiker's Guide to Python</a> has details on how to install Python and pip.

Getting Started
----------

Obtain your API token from your profile page (click your username in the top banner) under the **Edit Profile** tab. In Python, you can initialize an instance of *peyton* as follows:

```python
import peyton
throne = peyton.Throne(username='USERNAME', token="TOKEN")
```

With the Throne API instance you can then interact with Throne.ai:

```python
# View your XP
throne.user.get_xp()

# View your performance
throne.user.get_performance()

# Plot your historical score in a competition
throne.user.plot_score('English Premier League')

# Plot your edge in each competition
throne.user.plot_edge()

# Get historical data for a competition
throne.competition('NFL').get_historical_data()
my_historical_data = throne.historical_data

# Get competition data for a competition
throne.competition('NFL').get_competition_data()
my_competition_data = throne.competition_data

# Submit predictions 
throne.competition('NFL').submit(my_submission_df)

# Make an audible
throne.omaha()
```

We will look to provide documentation for the API once we expand its capabilities. 

**Please note that due to throttling limits you should SAVE your historical and competition data rather than reloading from our servers each time you run a script or Notebook.**

Peyton Discussion and Support
---------------------------

Please consult our Slack Channel at https://throneai.slack.com. For an invite, go to your profile pack and click 'Slack Invite'.
