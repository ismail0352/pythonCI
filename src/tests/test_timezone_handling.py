"""
Test timezone-related methods and functions.
"""
from __future__ import print_function

from datetime import datetime, timedelta
import re
from unittest import TestCase

import pytz

from frontend_utils.view_base import get_timezone_offset, local_2_utc, \
    utc_2_local


class TestTimezoneHandling(TestCase):

    def test_good_browsers(self):
        # (new Date()).toTimeString() from different browsers and OS's
        # This is a list of browsers and OS's that are "good" (that
        # return a time string in the format that we expect.)
        good_list = [
            # Chromium 35.0.1916.153 on Fedora 20
            ("08:01:18 GMT-0400 (EDT)", "GMT-0400"),
            # FireFox 32.0.3 on Windows 7
            ("09:06:42 GMT-0400 (Eastern Standard Time)", "GMT-0400"),
            # FireFox 32.0.2 on Windows 8.1
            ("09:22:29 GMT-0400 (Eastern Standard Time)", "GMT-0400"),
            # Google Chrome 37.0.2062.124m on Windows 8.1
            ("09:24:52 GMT-0400 (Eastern Daylight Time)", "GMT-0400"),
            # Internet Explorer 11.0.9600.17278
            ("09:28:03 GMT-0400 (Eastern Daylight Time)", "GMT-0400"),
        ]
        server_timezone = "Europe/Paris"
        for javascript_timestr, expected_result in good_list:
            result = get_timezone_offset(javascript_timestr, server_timezone)
            print("{0!r} -> {1!r}".format(javascript_timestr, result))
            self.assertEqual(result, expected_result)

    def test_bad_browsers(self):
        bad_list = [
            # Internet Explorer 8.0.7600.16385
            "09:11:58 EDT",
            # Some other weird, unsupported time string
            "Twelve O'Clock",
        ]
        server_timezone = "Europe/Paris"
        for bad_javascript_timestr in bad_list:
            result = get_timezone_offset(bad_javascript_timestr, server_timezone)
            print("{0!r} -> {1!r}".format(bad_javascript_timestr, result))
            # Assert that the result is in the expected format
            self.assertTrue(re.search(r"[+-]\d{4}$", result))

    def test_using_server_default(self):
        server_timezone = "Europe/Paris"
        tz1 = pytz.timezone(server_timezone)
        now = datetime.now()
        expected_offset = tz1.utcoffset(now)
        print("server_timezone for testing: ", server_timezone)
        print("Current time for testing: ", now)
        print("Expected timezone offset as timedelta:", expected_offset)
        ###
        result = get_timezone_offset("", server_timezone)
        ###
        result_offset_str = result[-5:]
        offset_hours = int(result_offset_str[1:3])
        offset_minutes = int(result_offset_str[3:5])
        result_offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        if result_offset_str[0] == '-':
            result_offset = timedelta(0) - result_offset
        print("Result from get_timezone_offset():", result)
        print("Resulting timezone offset:", result_offset_str)
        print("Resulting timezone offset as timedelta:", result_offset)
        print("Expected offset minus resulting offset (should be zero):",
              expected_offset - result_offset)
        self.assertEqual(expected_offset, result_offset)

    def test_local_2_utc(self):
        print()
        print("test_local_2_utc()")
        print()
        test_values = [
            ("2014-09-29 09:00:31", "GMT-0400", datetime(2014, 9, 29, 13, 0, 31)),
            ("2014-12-31 14:35:15", "CET+0100", datetime(2014, 12, 31, 13, 35, 15)),
        ]
        for local_time, timezone_offset, expected_result in test_values:
            result = local_2_utc(local_time, timezone_offset)
            print("local_2_utc({0!r}, {1!r}) -> {2!r}".format(
                local_time, timezone_offset, expected_result))
            self.assertEqual(expected_result, result)

    def test_utc_2_local(self):
        print()
        print("test_utc_2_local()")
        print()
        test_values = [
            ("2014-09-29 13:00:31", "GMT-0400", datetime(2014, 9, 29, 9, 0, 31)),
            ("2014-12-31 13:35:15", "CET+0100", datetime(2014, 12, 31, 14, 35, 15)),
        ]
        for utc_timestr, timezone_offset, expected_result in test_values:
            result = utc_2_local(utc_timestr, timezone_offset)
            print("utc_2_local({0!r}, {1!r}) -> {2!r}".format(
                utc_timestr, timezone_offset, expected_result))
            self.assertEqual(expected_result, result)

if __name__ == '__main__':
    unittest.main()
