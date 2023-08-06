# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
# Usage subject to license agreement
# hello@dativa.com for more information

from dativa.scrubber.tests import _BaseTest
from dativa.scrubber import ScrubberValidationError


class DateTests(_BaseTest):

    def test_date(self):
        self._test_filter(dirty_file="date/date_format.csv",
                          clean_file="date/date_format_clean.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%d-%m-%Y %H:%M:%S",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",
                                          "is_unique": False,
                                          "lookalike_match": False,
                                          "range_check": "rolling",
                                          "range_maximum": "10000",
                                          "range_minimum": "0",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "Date"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ])

    def test_date_1(self):
        self._test_filter(dirty_file="date/date_format.csv",
                          clean_file="date/date_format_clean1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%d-%m-%Y %H:%M:%S",
                                          "default_value": "",
                                          "fallback_mode": "remove_record",

                                          "is_unique": False,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "01-01-2028 00:00:00",
                                          "range_minimum": "01-01-2017 10:03:16",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "Date"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'quarantined',
                                  'description': 'Data quarantined',
                                  'df': [['30-03-2010 10:03:26'],
                                         ['31-02-2027 10:99:16'],
                                         ['05-04-2027 25:03:16']],

                              },
                          ])

    def test_date_2(self):
        self._test_filter(dirty_file="date/date_format.csv",
                          clean_file="date/date_format_clean2.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%d-%m-%Y %H:%M:%S",
                                          "default_value": "",
                                          "fallback_mode": "do_not_replace",

                                          "is_unique": False,
                                          "lookalike_match": False,
                                          "range_check": "none",
                                          "range_maximum": "",
                                          "range_minimum": "",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "Date"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 2,
                                  'category': 'ignored',
                                  'description': 'No changes made',
                                  'df': [['31-02-2027 10:99:16', '31-02-2027 10:99:16'],
                                         ['05-04-2027 25:03:16', '05-04-2027 25:03:16']],

                              },
                          ])

    def test_date_3(self):
        self._test_filter(dirty_file="date/date_format1.csv",
                          clean_file="date/date_format1_clean.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%d-%m-%Y",
                                          "default_value": "N/A",
                                          "fallback_mode": "remove_record",

                                          "is_unique": False,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "02-05-2021",
                                          "range_minimum": "01-01-2001",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "Date"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 10,
                                  'category': 'quarantined',
                                  'description': 'Data quarantined',
                                  'df': [['19-19-2001'],
                                         ['05-04-2103'],
                                         ['06-04-2103'],
                                         ['07-04-2103'],
                                         ['08-04-2103'],
                                         ['09-04-2103'],
                                         [None],
                                         ['748949+84'],
                                         ['231514'],
                                         ['45457']],

                              },
                          ]
                          )

    def test_date_4(self):
        self._test_filter(dirty_file="date/date_is_unique_dirty.csv",
                          clean_file="date/date_is_unique_cleaned.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%d/%m/%Y %H:%M:%S",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "24/12/2017 07:01:15",
                                          "range_minimum": "18/12/2017 07:01:15",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "Date"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 2,
                                  'category': 'quarantined',
                                  'description': 'Removed duplicates',
                                  'df': [['18/12/2017 07:01:15'],
                                         ['19/12/2017 07:01:15']],

                              },
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 1,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['25/12/2017 07:01:15', 'N/A']],

                              },
                          ])

    def test_date_5(self):
        self._test_filter(dirty_file="date/date_format_2.csv",
                          clean_file="date/date_format_2.csv",
                          config={'rules': [
                              {'field': 'PREV_CHECKIN_DATE',
                               'rule_type': 'Date',
                               'params': {'date_format': '%Y-%m-%d %H:%M:%S.%f', 'range_check': 'none',
                                          'fallback_mode': 'remove_record'}},
                              {'field': 'CHECKIN_DATE',
                               'rule_type': 'Date',
                               'params': {'date_format': '%Y-%m-%d %H:%M:%S.%f', 'range_check': 'none',
                                          'fallback_mode': 'remove_record'}}, ]},
                          csv_delimiter="|",
                          report=[])

    def test_date_6(self):
        self._test_filter(dirty_file="date/date_format_2.csv",
                          clean_file="date/date_format_2_clean.csv",
                          config={'rules': [
                              {'field': 'PREV_CHECKIN_DATE',
                               'rule_type': 'Date',
                               'params': {'date_format': '%Y/%m/%d %H:%M:%S.%f', 'range_check': 'none',
                                          'fallback_mode': 'remove_record'}},
                              {'field': 'CHECKIN_DATE',
                               'rule_type': 'Date',
                               'params': {'date_format': '%Y/%m/%d %H:%M:%S.%f', 'range_check': 'none',
                                          'fallback_mode': 'remove_record'}}, ]},
                          csv_delimiter="|",
                          report=[
                              {

                                  'field': 'PREV_CHECKIN_DATE',
                                  'rule': 'Date',
                                  'number_records': 11,
                                  'category': 'quarantined',
                                  'description': 'Data quarantined',
                                  'df': [['2018-02-28 00:00:00.000000'],
                                         ['2018-02-28 00:00:00.000000'],
                                         ['2018-02-25 00:00:00.000000'],
                                         ['2018-02-28 00:00:00.000000'],
                                         ['2018-02-27 00:00:00.000000'],
                                         ['2018-02-24 00:00:00.000000'],
                                         ['2018-02-28 00:00:00.000000'],
                                         ['2018-02-28 00:00:00.000000'],
                                         ['2018-02-28 00:00:00.000000'],
                                         ['2018-02-28 00:00:00.000000'],
                                         ['2018-02-28 00:00:00.000000']],

                              },
                          ])

    def test_date_epoch(self):
        self._test_filter(dirty_file="date/check_epoch_time.csv",
                          clean_file="date/check_epoch_time_cleaned1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%s",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "1511373354",
                                          "range_minimum": "1511344324",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "utc_air_start_epoch"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'utc_air_start_epoch',
                                  'rule': 'Date',
                                  'number_records': 14,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [[1511379769, 'N/A'],
                                         [1511343124, 'N/A'],
                                         [1511336569, 'N/A'],
                                         [1511329924, 'N/A'],
                                         [1511328724, 'N/A'],
                                         [1511322169, 'N/A'],
                                         [1511315524, 'N/A'],
                                         [1511314324, 'N/A'],
                                         [1511394199, 'N/A'],
                                         [1511393209, 'N/A'],
                                         [1511386999, 'N/A'],
                                         [1511386009, 'N/A'],
                                         [1511379799, 'N/A'],
                                         [1511378809, 'N/A']],

                              },
                          ])

    def test_date_epoch_2(self):
        self._test_filter(dirty_file="date/check_epoch_time.csv",
                          clean_file="date/check_epoch_time_cleaned1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%s",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "1511373354",
                                          "range_minimum": "banana",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "utc_air_start_epoch"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)

    def test_date_range_error(self):
        self._test_filter(dirty_file="date/check_epoch_time.csv",
                          clean_file="date/check_epoch_time_cleaned1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%s",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_minimum": "1511344324",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "utc_air_start_epoch"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)

    def test_date_range_error_2(self):
        self._test_filter(dirty_file="date/check_epoch_time.csv",
                          clean_file="date/check_epoch_time_cleaned1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%s",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "1511373354",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "utc_air_start_epoch"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)

    def test_date_range_error_3(self):
        self._test_filter(dirty_file="date/check_epoch_time.csv",
                          clean_file="date/check_epoch_time_cleaned1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%s",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "1st January 2001",
                                          "range_minimum": "1511344324",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "utc_air_start_epoch"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)

    def test_date_range_error_4(self):
        self._test_filter(dirty_file="date/check_epoch_time.csv",
                          clean_file="date/check_epoch_time_cleaned1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%s",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "1511373354",
                                          "range_minimum": "1st January 2001",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "utc_air_start_epoch"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)

    def test_date_range_error_5(self):
        self._test_filter(dirty_file="date/check_epoch_time.csv",
                          clean_file="date/check_epoch_time_cleaned1.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%s",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",

                                          "is_unique": True,
                                          "lookalike_match": False,
                                          "range_check": "fixed",
                                          "range_maximum": "1511373354",
                                          "range_minimum": "2511344324",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "utc_air_start_epoch"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)

    def test_date_error_6(self):
        self._test_filter(dirty_file="date/date_format.csv",
                          clean_file="date/date_format_clean.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%d-%m-%Y %H:%M:%S",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",
                                          "is_unique": False,
                                          "lookalike_match": False,
                                          "range_check": "rolling",
                                          "range_maximum": "10000",
                                          "range_minimum": "1st January 2000",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "Date"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)

    def test_date_error_7(self):
        self._test_filter(dirty_file="date/date_format.csv",
                          clean_file="date/date_format_clean.csv",
                          config={
                              "rules": [
                                  {
                                      "append_results": False,
                                      "params": {
                                          "attempt_closest_match": False,
                                          "date_format": "%d-%m-%Y %H:%M:%S",
                                          "default_value": "N/A",
                                          "fallback_mode": "use_default",
                                          "is_unique": False,
                                          "lookalike_match": False,
                                          "range_check": "rolling",
                                          "range_maximum": "1st January 2000",
                                          "range_minimum": "0",
                                          "skip_blank": False,
                                          "string_distance_threshold": 0.7
                                      },
                                      "rule_type": "Date",
                                      "field": "Date"
                                  }
                              ]
                          },
                          report=[
                              {

                                  'field': 'Date',
                                  'rule': 'Date',
                                  'number_records': 3,
                                  'category': 'replaced',
                                  'description': 'Replaced with default value',
                                  'df': [['30-03-2010 10:03:26', 'N/A'],
                                         ['31-02-2027 10:99:16', 'N/A'],
                                         ['05-04-2027 25:03:16', 'N/A']],

                              },
                          ],
                          expected_error=ScrubberValidationError)
