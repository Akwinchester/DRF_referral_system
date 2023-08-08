from django.db import models


class UserProfile(models.Model):
  phone = models.CharField(max_length=16, unique=True)
  invite_code = models.CharField(max_length=6)
  confirmation_code = models.CharField(max_length=4)
  referred_users = models.ManyToManyField('self',through='Referral',symmetrical=False)
  last_login = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.phone


class Referral(models.Model):
  from_user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='referrals_made'
  )

  to_user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='referrals_received'
  )