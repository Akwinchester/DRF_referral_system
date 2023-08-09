from typing import Dict

from referral_system.models import UserProfile
from referral_system.services.utils import logger, get_current_time

# Добавляет пользователя в список приглашенных по конкретному invite_code
def add_referral(request, invite_code: str) -> Dict[str, str]:
    try:
        inviting_user = UserProfile.objects.get(invite_code=invite_code)
        logger.info(f"({get_current_time()}) В БД найден пользователь по invite_code: {invite_code}")
    except UserProfile.DoesNotExist as e:
        logger.info(f"({get_current_time()}) Ошибка в add_referral\nОшибка:\n{e}")
        return{"error": "Invalid invite code"}

    inviting_user.referred_users.add(request.user)
    inviting_user.save()
    logger.info(f"({get_current_time()}) Пользователь {request.user} добавлен в список приглашенных пользователем {inviting_user}")
    return {"success": "Referrer added"}
