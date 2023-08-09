import logging
from datetime import datetime
from ..models import UserProfile

logger = logging.getLogger('referral_system')

def get_current_time():
    return  datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def jwt_payload_handler(user):
    return {'user_id': user.id}


def jwt_get_user_id_from_payload_handler(payload):
    user_id = payload.get('user_id')
    return UserProfile.objects.get(id=user_id)
