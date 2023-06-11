from base.models import Team

def navbar_context(request):
    pic_dict = {
        'jakeyoder' : 'base/img/profile_pics/amish.jpeg',
        'sharonblair' : 'base/img/profile_pics/brady.jpeg',
        'bobsmith' : 'base/img/profile_pics/bruisers.gif',
        'jaysoncromly' : 'base/img/profile_pics/dawgs.gif',
        'ericblair' : 'base/img/profile_pics/force.jpg',
        'mattsevey' : 'base/img/profile_pics/mattimine.gif',
        'tellyfricke' : 'base/img/profile_pics/secrets.png',
        'vinceberry' : 'base/img/profile_pics/specials.png',
        'robfricke' : 'base/img/profile_pics/tricksters.gif',
        'jacobcromly' : 'base/img/profile_pics/twisters.gif',
        'trevorblair' : 'base/img/profile_pics/tycoons.jpeg',
        'troyblair' : 'base/img/profile_pics/warriors.jpeg',
        'team13' : 'base/img/profile_pics/team-13.png',
        'team14' : 'base/img/profile_pics/team-14.png',
    }
    user_team_pk = None
    user_team = None
    commissioner = None

    if request.user.is_authenticated:
        user_team = Team.objects.filter(owner=request.user).first()
        if user_team:
            user_team_pk = user_team.pk
        else:
            user_team_pk = None
        commissioner = Team.objects.filter(commissioner=True).first()

    context = {
        'pic_dict': pic_dict,
        'commissioner': commissioner.owner if commissioner else None,
        'user_team_pk': user_team_pk,
        'teams': Team.objects.all().order_by('draft_order'),
        'user_team': user_team,
    }


    return context
