# Import necessary libraries
from django.shortcuts import render
from django.http import HttpResponse
import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import instaloader  # Import Instaloader

from .forms import ProfileSearchForm  # Update with your form import path

# Read data from CSV file
df = pd.read_csv('train.csv')

# Define features and labels (customize based on your feature extraction)
# Here, we use 'external URL' and '#posts' as example features
X = df[['external URL', '#posts']]
y = df['fake']

# Create a Random Forest Classifier with adjusted hyperparameters
clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

# Train the model
clf.fit(X, y)

# Function to predict fake accounts

def predict_fake_account(request):
    prediction = None
    followers_count = None
    following_count = None
    accounturl = None  # Initialize accounturl variable

    if request.method == 'POST':
        form = ProfileSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['text_input']
            try:
                ig = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(ig.context, username)

                posts_on_website = profile.mediacount
                followers_count = profile.followers
                following_count = profile.followees

                user_input = [[posts_on_website, followers_count]]

                prediction = clf.predict(user_input)[0]
                accounturl = username  # Set accounturl to username

            except Exception as e:
                return HttpResponse(f'An error occurred: {str(e)}')

    else:
        form = ProfileSearchForm()

    return render(request, 'index.html', {'form': form, 'prediction': prediction, 'followers': followers_count, 'following': following_count, 'username': accounturl})