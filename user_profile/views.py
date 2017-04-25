from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required # imports login_required tag
from user_profile.models import UserProfile
from user_profile.forms import UserProfileForm

def profile(request):
    userProfile = userProfile.object.get(user=request.user)
    return render(request, 'user/profile.html', {'userProfile': userProfile})

# tag that restricts only when you're not logged in
@login_required
def update_profile(request):
    userProfile = userProfile.object.get(user=request.user)
    form = UserProfileForm()
    return render_to_response('user_profile/update_profile.html', {'form':form}, RequestContext(request))

@login_required
def your_profile(request):
    userProfile = userProfile.object.get(user=request.user)
    return render(request, 'user/your_profile.html', {'userProfile': userProfile})
