from app.place_order import *
from angelproject.settings import *
from .get_trade import * 
from .history import *
from .margin import *
from . LTP import *
from .imports import *
from .individual_order import *
# from .update_order_status import *


from celery import app as celery_app

__all__ = ('celery_app',)