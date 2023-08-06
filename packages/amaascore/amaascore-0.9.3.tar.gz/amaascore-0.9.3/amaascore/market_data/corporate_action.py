from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import date, datetime
from dateutil.parser import parse
from decimal import Decimal
import sys
import pytz
import json

from amaascore.core.amaas_model import AMaaSModel


class CorporateAction(AMaaSModel):

    def __init__(self, asset_manager_id, asset_id, business_date, event_detail, 
                 client_id, event_type, active=True, *args, **kwargs):
        """

        :param asset_manager_id: The asset_manager_id of the asset for which we have the price.  Can be 0 for shared.
        :param asset_id: The equity/fund asset this corporate action is associated with
        :param business_date: The ex-date of this event
        :param event_detail: The details of this corporate action event, stored in json format
        :param event_type: The type of this event, "dividend" or "split".
        :param active: The boolean status of the rate.  This is to allow corrections.
        """
        self.asset_manager_id = asset_manager_id
        self.asset_id = asset_id
        self.business_date = business_date
        self.event_type = event_type
        self.event_detail = event_detail
        self.active = active
        self.client_id = client_id
        super(CorporateAction, self).__init__(*args, **kwargs)
        

    @property
    def event_detail(self):
        return self._event_detail

    @event_detail.setter
    def event_detail(self, event_detail):
        """
        :param event_detail:
        :return:
        """
        if event_detail is not None:
            if isinstance(event_detail, str):
                self._event_detail = event_detail
            else:
                try:
                    for key, val in event_detail.items():
                        if isinstance(val, date):
                            event_detail[key] = str(val)
                    self._event_detail = json.dumps(event_detail)
                except TypeError:
                    raise TypeError('Passed in event detail object are not json serializable.Please check the format')


    @property
    def business_date(self):
        return self._business_date


    @business_date.setter
    def business_date(self, business_date):
        """
        Force the business_date to always be a date
        :param business_date:
        :return:
        """
        if business_date is not None:
            if isinstance(business_date, str):
                self._business_date = parse(business_date).date()
            else:
                self._business_date= business_date   