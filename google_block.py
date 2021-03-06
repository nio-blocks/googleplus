from datetime import datetime

from nio.properties import VersionProperty, StringProperty, \
    TimeDeltaProperty, IntProperty
from nio.signal.base import Signal

from .rest_polling.rest_block import RESTPolling


class GooglePlusSignal(Signal):

    def __init__(self, data):
        super().__init__()
        for k in data:
            setattr(self, k, data[k])


class GooglePlus(RESTPolling):

    version = VersionProperty("1.0.1")
    URL_FORMAT = ("https://www.googleapis.com/plus/v1/activities"
                  "?query={0}&orderBy=recent&maxResults={1}&key={2}")

    dev_key = StringProperty(title='Developer Key',
                             default='[[GOOGLE_API_KEY]]')
    lookback = TimeDeltaProperty(title='Lookback Period',
                                 default={"seconds": 300})
    limit = IntProperty(title='Limit', default=20)

    def __init__(self):
        super().__init__()
        self._paging_field = 'nextPageToken'
        self._created_field = 'published'
        self._page_token = None

    def configure(self, context):
        super().configure(context)
        lb = self._unix_time(datetime.utcnow() - self.lookback())
        self._freshest = [lb] * self._n_queries

    def _process_response(self, resp):
        signals = []
        paging = False
        status = resp.status_code
        if status == 304:
            return [], paging

        resp = resp.json()
        fresh_posts = posts = resp.get('items', [])
        self._page_token = resp.get(self._paging_field)
        self.logger.debug("Google+ response contains %d posts" % len(posts))

        if len(posts) > 0:
            self.update_freshness(posts)
            fresh_posts = self.find_fresh_posts(posts)
            paging = len(fresh_posts) == len(posts)

        signals = [GooglePlusSignal(p) for p in fresh_posts]
        self.logger.debug("Found %d fresh posts" % len(signals))

        return signals, paging

    def _prepare_url(self, paging=False):
        headers = {"Content-Type": "application/json"}
        if self.etag is not None:
            headers['If-None-Match'] = self.etag
        if self.modified is not None:
            headers['If-Modified-Since'] = self._modified

        self.url = self.URL_FORMAT.format(
            self.current_query,
            self.limit(),
            self.dev_key()
        )
        if paging:
            self.url = "%s&pageToken=%s" % (self.url, self._page_token)

        return headers

    def _get_post_id(self, post):
        return getattr(post, 'id', None)
