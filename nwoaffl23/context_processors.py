from base.models import Team

def navbar_context(request):
    user_team_pk = None
    commissioner = None

    if request.user.is_authenticated:
        user_team = Team.objects.filter(owner=request.user).first()
        if user_team:
            user_team_pk = user_team.pk
        commissioner = Team.objects.filter(commissioner=True).first()

    context = {
        'commissioner': commissioner.owner if commissioner else None,
        'user_team_pk': user_team_pk,
        'teams': Team.objects.all()
    }


    return context
