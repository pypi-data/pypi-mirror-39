from __future__ import absolute_import, division, print_function, unicode_literals

from amaasutils.random_utils import random_string, random_decimal
from datetime import datetime, date, timedelta
import pytz
import random

from amaascore.market_data.eod_price import EODPrice
from amaascore.market_data.fx_rate import FXRate
from amaascore.market_data.curve import Curve
from amaascore.market_data.quote import Quote
from amaascore.market_data.corporate_action import CorporateAction


def generate_eod_price(asset_manager_id=0, asset_id=None, business_date=date.today(), price=None):
    eod_price = EODPrice(asset_manager_id=asset_manager_id,
                         asset_id=asset_id or random_string(10),
                         business_date=business_date,
                         price=price or random_decimal())
    return eod_price


def generate_fx_rate(asset_manager_id=0, asset_id=None, rate_timestamp=None, rate=None, business_date=None,
                     rate_type='EOD'):
    now = datetime.utcnow().replace(tzinfo=pytz.utc, microsecond=0)
    rate_timestamp = rate_timestamp or now
    business_date = business_date or rate_timestamp.date() if type(rate_timestamp) == datetime else rate_timestamp
    fx_rate = FXRate(asset_manager_id=asset_manager_id,
                     asset_id=asset_id or random.choice(['USDJPY', 'USDSGD', 'EURUSD']),
                     business_date=business_date,
                     rate_timestamp=rate_timestamp,
                     rate=rate or random_decimal(),
                     rate_type=rate_type)
    return fx_rate


def generate_quote(asset_manager_id=0, asset_id=None, bid=None, ask=None):
    quote = Quote(asset_manager_id=asset_manager_id,
                  asset_id=asset_id or random_string(10),
                  bid=bid or random_decimal(),
                  ask=ask or random_decimal(),
                  quote_datetime=datetime.utcnow())
    return quote


def generate_curve(client_id = None, asset_manager_id = 0, asset_id = None, fixing_type = None, curve_timestamp = None, 
                    curve_type = None, additional = None, active = True, curve_rates = None, business_date = None):
    time = datetime.utcnow().replace(tzinfo=pytz.utc)
    curve = Curve(asset_manager_id=asset_manager_id,
                  asset_id = asset_id or 'EURUSD',
                  fixing_type = fixing_type or 'EOD',
                  business_date = business_date or time.date(),
                  curve_timestamp = curve_timestamp or time,
                  client_id = client_id or random.randint(1, 2**31-1),
                  curve_type = curve_type or 'fx forward',
                  additional = additional or {'tenor_dates': {'1M': (timedelta(days=30) + (business_date or time.date())).isoformat(), 
                                                              '1W': (timedelta(days=7) + (business_date or time.date())).isoformat()}},
                  active =  active or True,
                  curve_rates = curve_rates or '{"1M": "1.05033", "1W": "1.049202"}'
                 )
    return curve


def generate_corporate_action(client_id=None, asset_manager_id=0, asset_id=None, event_type=None, event_detail=None,
                              business_date=None, active=1):
    random_event_detail = {'payment_date': date(2013, 3, 2),
                           'amount_per_share': 2,
                           'currency': 'USD'}
    corporate_action = CorporateAction(asset_manager_id=asset_manager_id,
                                       asset_id=asset_id or random_string(10),
                                       event_type='dividend',
                                       business_date=business_date or datetime.utcnow().date(),
                                       client_id=client_id or random.randint(1, 2**31-1),
                                       active=active or 1,
                                       event_detail=event_detail or random_event_detail)
    return corporate_action