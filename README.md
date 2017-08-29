GooglePlus
==========
Polls Google Plus for public posts. Official documentation of [Google Plus API](https://developers.google.com/+/api/latest/activities/search).

Properties
----------
- **dev_key**: Google API credentials.
- **include_query**: Whether to include queries in request to Google Plus.
- **limit**: Number of posts notified on each url request.
- **lookback**: On block start, look back this amount of time to grab old posts.
- **polling_interval**: How often API is polled. When using more than one query. Each query will be polled at a period equal to the `polling_interval` times the number of `queries`.
- **queries**: List of queries to search public posts for. Note that multi-word queries will search for posts that have all of the words but not as a single string.
- **retry_interval**: When a url request fails, how long to wait before attempting to try again.
- **retry_limit**: Number of times to retry on a poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: Creates a new signal for each Google Plus Post. Every field on the Post will become a signal attribute. Official documentation on the repsonse fields from Goolge Plus [here](https://developers.google.com/+/api/latest/activities#resource). See below for a list of commonly include attributes, but note that not all will be included on every signal.

Commands
--------
None

Dependencies
------------
requests

Output Example
--------------
```
{
  id: string,
  actor: {
    displayName: string
  },
  title: string,
  object: {
    content: string
  },
  url: string,
  actor: {
    id: string,
    url: string,
    image: {
      url: string
    }
  },
  published: datetime,
  updated: datetime
}
```

