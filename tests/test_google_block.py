from ..google_block import GooglePlus
from unittest.mock import patch
from requests import Response
from datetime import datetime, timedelta
from nio.testing.block_test_case import NIOBlockTestCase
from threading import Event


class GPTestBlk(GooglePlus):
    def __init__(self, event):
        super().__init__()
        self._event = event

    def _paging(self):
        self._locked_poll(True)
        self._event.set()

class TestGooglePlus(NIOBlockTestCase):

    @patch("requests.get")
    @patch("requests.Response.json")
    @patch.object(GooglePlus, 'created_epoch')
    def test_process_responses(self, mock_epoch, mock_json, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 200
        mock_epoch.return_value = 23
        mock_json.return_value = {
            'items': [
                {'key': 'val'}
            ]
        }
        e = Event()
        blk = GPTestBlk(e)
        self.configure_block(blk, {
            "log_level": "DEBUG",
            "polling_interval": {
                "seconds": 1
            },
            "retry_interval": {
                "seconds": 1
            },
            "queries": [
                "foobar"
            ],
            "limit": 2,
        })
        blk._freshest = [22]

        blk.start()
        e.wait(2)

        self.assertEqual(blk._freshest, [23])
        self.assert_num_signals_notified(1)

        blk.stop()

    @patch("requests.get")
    @patch("requests.Response.json")
    @patch.object(GooglePlus, 'created_epoch')
    def test_multiple_queries(self, mock_epoch, mock_json, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 200
        mock_epoch.return_value = 23
        mock_json.return_value = {
            'items': [
                {'id': 'id1', 'key': 'val1'},
                {'id': 'id2', 'key': 'val2'},
                {'id': 'id3', 'key': 'val3'}
            ]
        }
        e = Event()
        blk = GPTestBlk(e)
        self.configure_block(blk, {
            "log_level": "DEBUG",
            "polling_interval": {
                "seconds": 1
            },
            "retry_interval": {
                "seconds": 1
            },
            "queries": [
                "foobar",
                "foo",
                "bar"
            ],
            "limit": 4,
        })
        blk._freshest = [22, 22, 22]
        blk.start()
        e.wait(2)
        e.clear()
        self.assert_num_signals_notified(3)
        # second query should only emit one signal because
        # the others are duplicates from first query.
        mock_json.return_value = {
            'items': [
                {'id': 'id1', 'key': 'val1'},
                {'id': 'id2', 'key': 'val2'},
                {'id': 'id3', 'key': 'val3'},
                {'id': 'id4', 'key': 'val4'}
            ]
        }
        e.wait(2)
        e.clear()
        self.assert_num_signals_notified(4)
        e.wait(2)
        e.clear()
        self.assert_num_signals_notified(4)
        blk.stop()
