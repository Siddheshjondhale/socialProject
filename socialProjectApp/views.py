from django.shortcuts import render
import re

# # Create your views here.
# def Home1(request):
#     url = 'https://www.instagram.com/bard/'
#     username = get_username_from_insta_profile_url(url)
#     print(username)
 
#     context = {
#     'username': username
#     }

#     return render(request,"index.html",context)


# def get_username_from_insta_profile_url(url):
#   username_pattern = r'/(.*?)/'
#   matches = re.findall(username_pattern, url)
#   username = matches[0]
#   return username

from django.shortcuts import render
from django.http import HttpResponseRedirect
from urllib.parse import quote

from socialProjectApp.forms import ProfileSearchForm

def search_profile(request):
    if request.method == 'POST':
        form = ProfileSearchForm(request.POST)
        if form.is_valid():
            social_media = form.cleaned_data['social_media']
            username = form.cleaned_data['username']

            # Map social media choices to their respective URL patterns
            social_media_urls = {
                'instagram': f'https://www.instagram.com/{quote(username)}/',
                'facebook': f'https://www.facebook.com/{quote(username)}/',
                'twitter': f'https://twitter.com/{quote(username)}/',
            }

            if social_media in social_media_urls:
                return HttpResponseRedirect(social_media_urls[social_media])

    else:
        form = ProfileSearchForm()

    return render(request, 'index.html', {'form': form})





