from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Profile, User
from accounts.forms import ProfileForm
from .models import Connection

@login_required
def dashboard(request):
    # Suggested matches (simple logic: opposite gender, not connected)
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        return redirect('edit_profile')

    matches = Profile.objects.exclude(user=request.user)
    
    if user_profile.gender:
        target_gender = 'F' if user_profile.gender == 'M' else 'M'
        matches = matches.filter(gender=target_gender)

    # Exclude already connected users
    sent_requests = Connection.objects.filter(sender=request.user).values_list('receiver_id', flat=True)
    received_requests = Connection.objects.filter(receiver=request.user).values_list('sender_id', flat=True)
    
    matches = matches.exclude(user__id__in=sent_requests).exclude(user__id__in=received_requests)

    return render(request, 'profiles/dashboard.html', {'matches': matches})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def search_profiles(request):
    query = request.GET.get('q')
    profiles = Profile.objects.exclude(user=request.user)
    
    if query:
        profiles = profiles.filter(
            Q(location__icontains=query) | 
            Q(profession__icontains=query) |
            Q(religion__icontains=query) |
            Q(caste__icontains=query)
        )
    
    return render(request, 'profiles/search.html', {'profiles': profiles})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    connection = Connection.objects.filter(
        (Q(sender=request.user, receiver=profile.user) | Q(sender=profile.user, receiver=request.user))
    ).first()
    
    return render(request, 'profiles/profile_detail.html', {'profile': profile, 'connection': connection})
