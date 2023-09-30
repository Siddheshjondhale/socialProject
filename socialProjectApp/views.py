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
    
    if request.method == 'POST':
        form = ProfileSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['text_input']
            # username='dsd'
            try:
                # Initialize Instaloader
                ig = instaloader.Instaloader()
                
                # Fetch the details of the provided username using Instaloader
                profile = instaloader.Profile.from_username(ig.context, username)

                # Extract relevant features
                posts_on_website = profile.mediacount
                followers_count = profile.followers
                following_count = profile.followees

                # Make prediction based on extracted features
                user_input = [
                [posts_on_website, followers_count]
                ]

                prediction = clf.predict(user_input)[0]

                return render(request, 'result.html', {'prediction': prediction, 'followers': followers_count, 'following': following_count})
            except Exception as e:
                return HttpResponse(f'An error occurred: {str(e)}')
    
    else:
        form = ProfileSearchForm()

    return render(request, 'index.html', {'form': form})
