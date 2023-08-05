""" Brottsplatskartan API """

import datetime
import time
from typing import Union

import requests

ATTRIBUTION = "Information provided by brottsplatskartan.se"
BROTTS_URL = "https://brottsplatskartan.se/api"


class BrottsplatsKartan: # pylint: disable=too-few-public-methods
    """ Brottsplatskartan API wrapper. """

    def __init__(self, app='bpk', area=None, longitude=None, latitude=None):
        """ Setup initial brottsplatskartan configuration. """

        self.parameters = {"app": app}

        if area:
            self.url = BROTTS_URL + "/events"
            self.parameters["area"] = area
        elif longitude and latitude:
            self.url = BROTTS_URL + "/eventsNearby"
            self.parameters["lat"] = latitude
            self.parameters["lng"] = longitude
        else:
            # Missing parameters. Using default values.
            self.url = BROTTS_URL + "/events"
            self.parameters["area"] = "Stockholms län"

    @staticmethod
    def _get_datetime_as_ymd(date: time.struct_time) -> datetime.datetime:

        datetime_ymd = datetime.datetime(
            date.tm_year, date.tm_mon, date.tm_mday
        )

        return datetime_ymd

    def get_incidents(self) -> Union[list, bool]:
        """ Get today's incidents. """
        brotts_entries_left = True
        incidents_today = []
        url = self.url

        while brotts_entries_left:

            requests_response = requests.get(
                url, params=self.parameters)

            rate_limited = requests_response.headers.get('x-ratelimit-reset')
            if rate_limited:
                print("You have been rate limited until " +
                      time.strftime(
                          '%Y-%m-%d %H:%M:%S%z',
                          time.localtime(rate_limited)
                      ))
                return False

            requests_response = requests_response.json()

            incidents = requests_response.get("data")
            if not incidents:
                break

            datetime_today = datetime.date.today()
            datetime_today_as_time = time.strptime(
                str(datetime_today), "%Y-%m-%d"
            )
            today_date_ymd = self._get_datetime_as_ymd(datetime_today_as_time)

            for incident in incidents:
                incident_pubdate = incident["pubdate_iso8601"]
                incident_date = time.strptime(
                    incident_pubdate, "%Y-%m-%dT%H:%M:%S%z"
                )
                incident_date_ymd = self._get_datetime_as_ymd(incident_date)

                if today_date_ymd == incident_date_ymd:
                    incidents_today.append(incident)
                else:
                    brotts_entries_left = False
                    break

            if requests_response.get("links"):
                url = requests_response["links"]["next_page_url"]
            else:
                break

        return incidents_today
