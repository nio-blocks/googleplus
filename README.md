GooglePlus
==========

Polls Google Plus for public posts. Official documentation of [Google Plus API](https://developers.google.com/+/api/latest/activities/search).

Properties
--------------

-   **queries**: List of queries to search public posts for. Note that multi-word queries will search for posts that have all of the words but not as a single string.
-   **dev_key**: API credentials.
-   **polling_interval**: How often API is polled. When using more than one query. Each query will be polled at a period equal to the `polling_interval` times the number of `queries`.
-   **retry_interval**: When a url request fails, how long to wait before attempting to try again.
-   **retry_limit**: When a url request fails, number of times to attempt a retry before giving up.
-   **lookback**: On block start, look back this amount of time to grab old posts.
-   **limit**: Number of posts notified on each url request.

Commands
----------------
None

Input
-------
None

Output
---------
Creates a new signal for each Google Plus Post. Every field on the Post will become a signal attribute. Official documentation on the repsonse fields from Goolge Plus [here](https://developers.google.com/+/api/latest/activities#resource). The following is a list of commonly include attributes, but note that not all will be included on every signal:

-   `id`
-   `actor`
  -   `displayName`
-   `title`
-   `object`
  -   `content`
-   `url`
-   `actor`
  -   `image`
  -   `url`
-   `published`
-   `updated`
