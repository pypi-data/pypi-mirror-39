![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# politico-civic-campaign-tracker

### Quickstart

1. Install the app.

  ```
  $ pip install politico-civic-campaign-tracker
  ```

2. Add the app to your Django project and configure settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'tracker',
  ]

  #########################
  # tracker settings

  TRACKER_SECRET_KEY = ''
  TRACKER_AWS_ACCESS_KEY_ID = ''
  TRACKER_AWS_SECRET_ACCESS_KEY = ''
  TRACKER_AWS_REGION = ''
  TRACKER_AWS_S3_BUCKET = ''
  TRACKER_CLOUDFRONT_ALTERNATE_DOMAIN = ''
  TRACKER_S3_UPLOAD_ROOT = ''
  ```

### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd tracker/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/tracker"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```

### Slack Workflows

#### Changing A Candidate Rating

 1. A candidate is selected:
   - Editor types `/2020-rating` in any channel on Slack.
   - A dropdown list of candidate names appears on their phone and they choose one.

      OR

   - Editor types `/2020-rating CANDIDATE_NAME` in any channel on Slack.


 2. A form appears on their phone with the candidate's win and run rating.

 3. Editor changes the appropriate rating, and clicks "Save".

 4. New message is posted in the `2020-tracker` Slack channel confirming that the candidate's rating has been changed.

#### Adding a Quote

 1. Reporter types `/2020-quote` in any channel on Slack.

 2. A form appears on their phone.

 3. Reporter fills out:
  - Who said it?
  - What did they say?
  - Link to the quote if available (e.g. Tweet, Press Release, etc)


 4. New quote is added to the tracker page and the `2020-tracker` Slack channel

#### Adding an Endorsement

 1. Reporter types `/2020-endorse` in any channel on Slack.

 2. A form appears on their phone.

 3. Reporter chooses which candidates was endorsed from a dropdown list

 4. Reporter also fills out:
  - Who did the endorsing?
  - Key quote from the endorsement
  - Link to the endorsement if available (e.g. Tweet, Press Release, etc)


 5. New endorsement is added to the tracker page and the `2020-tracker` Slack channel

#### Ambiguous Tweet Is Tagged

 1. Message is posted in the `2020-tracker` Slack channel with:
  - A `@mention` to the reporter who tweeted the ambiguous tweet
  - The tweet in question
  - A dropdown list with all the active candidates


 2. Reporter or editor choses a candidate from the dropdown list.

 3. The dropdown is replaced with a sentence saying the tweet has been assigned to the specific candidate.


### Twitter Workflow

##### Getting on the whitelist

Ask the interactives team to get your Twitter handle on the whitelist of Twitter accounts that can tweet at our bot and get their content onto our pages.

##### Tweeting reportage at the bot

1. Write a tweet that includes the candidate's name and @-mentions the bot. Example:

> Beto O'Rourke will announce his candidacy today at a town hall in Austin, Texas. @tracking2020

That's it! The bot will retweet this tweet, and the tweet will be embedded on our Beto O'Rourke page.

Sometimes, we will be unable to determine what candidate the tweet is about. For example:

> Joe Biden attacked Bernie Sanders' free college plan as "naive, wishful thinking." @tracking2020

We don't know if this is about Joe Biden or Bernie Sanders. In that case, see the [ambiguous tweet is tagged docs](#ambiguous-tweet-is-tagged) above.

##### Candidate quotes via the bot

You can also quote tweets and leave comments on them in the quote. Just make sure you tag the bot and name the candidate.

> Kamala Harris announcing her support for universal basic income via Twitter is a sign of how campaigning has changed in the modern era. https://twitter.com/KamalaHarris/status/1069638903378952193

This will embed your tweet and show the tweet you quoted.

Sometimes, a candidate will say something important on Twitter, and we want to send that quote in with no context. You can leverage the bot to do this quickly by quote tweeting the important tweet, and _only_ tagging the bot. For example:

> @tracking2020 https://twitter.com/CoryBooker/status/1068271280082886657

In this case, because no context was added, we will embed _just_ the quoted tweet on the page.

However, if you have time, we would prefer you use Slack to add this quote, because we can get more data about the quote from there. See [the docs](#adding-a-quote) above.