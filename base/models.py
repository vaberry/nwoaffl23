from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    commissioner = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='team_profile_pictures/', default='team_profile_pictures/person.svg')
    draft_order = models.IntegerField()
    team_new_trade = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Team)
def create_picks(sender, instance, created, **kwargs):

    if created:
        draft_order = instance.draft_order
        years = [2023, 2024]
        for year in years:
            for round_num in range(1, 16):
                pick = Pick.objects.create(
                    original_owner=instance,
                    current_owner=instance,
                    year=year,
                    round=round_num,
                    number=draft_order
                )
                pick.save()

class Pick(models.Model):
    original_owner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='original_picks')
    current_owner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='current_picks')
    year = models.IntegerField()
    round = models.IntegerField()
    number = models.IntegerField()
    selection = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Year: {self.year}, Round: {self.round}, Number: {self.number}"

class Trade(models.Model):
    STATUS_CHOICES = [
        ('STARTED', 'Started'),
        ('PROPOSED', 'Proposed'),
        ('COUNTERED', 'Countered'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    date_completed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='STARTED')
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='trades_team_one')
    team_one_accepted = models.BooleanField(default=False)
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='trades_team_two', blank=True, null=True)
    team_two_accepted = models.BooleanField(default=False)
    team_one_sends = models.ManyToManyField(Pick, related_name='trade_team_one_sends')
    team_two_sends = models.ManyToManyField(Pick, related_name='trade_team_two_sends')
    current_proposer = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='current_proposer', default=None, blank=True, null=True)
    extra_details = models.TextField(blank=True, null=True)
    # team_one_viewed = models.BooleanField(default=True)
    # team_two_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Trade ID: {self.pk}"
