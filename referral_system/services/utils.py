import logging
from datetime import datetime

logger = logging.getLogger('referral_system')

def get_current_time():
    return  datetime.now().strftime('%Y-%m-%d %H:%M:%S')