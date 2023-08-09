from referral_system.models import UserProfile


def add_referal(request, invite_code):
    try:
        inviting_user = UserProfile.objects.get(invite_code=invite_code)
    except UserProfile.DoesNotExist:
        return{"error": "Invalid invite code"}

    inviting_user.referred_users.add(request.user)
    inviting_user.save()

    return {"success": "Referrer added"}
