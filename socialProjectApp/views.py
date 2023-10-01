# Import necessary libraries
import csv
from io import TextIOWrapper
import tempfile
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
        form = ProfileSearchForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['text_input']
            csv_file = form.cleaned_data['csv_file']

            # Check if it's a CSV file
            if csv_file and not csv_file.name.endswith('.csv'):
                return HttpResponse('Invalid file format. Please upload a CSV file.')

            # Initialize a list to store the usernames
            usernames = []

            # If a CSV file is uploaded, read the usernames from it
            if csv_file:
                csv_data = TextIOWrapper(csv_file.file, encoding='utf-8-sig')
                reader = csv.reader(csv_data)
                for row in reader:
                    usernames.append(row[0])  # Assuming the usernames are in the first column

            # If a single username is provided in the text input, add it to the list
            if username:
                usernames.append(username)

            # Process the usernames
            output_data = []
            for username in usernames:
                try:
                    ig = instaloader.Instaloader()
                    profile = instaloader.Profile.from_username(ig.context, username)
                    posts_on_website = profile.mediacount
                    followers_count = profile.followers
                    following_count = profile.followees
                    user_input = [[posts_on_website, followers_count]]
                    prediction = clf.predict(user_input)[0]
                    output_data.append([username, 'Fake' if prediction == 1 else 'Genuine'])
                except Exception as e:
                    output_data.append([username, 'Invalid username'])

            # Create a temporary CSV file for the results
            with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as temp_file:
                writer = csv.writer(temp_file)
                writer.writerow(['Username', 'Status'])
                writer.writerows(output_data)

            # Generate a response with the CSV file
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="results.csv"'
            with open(temp_file.name, 'rb') as tf:
                response.write(tf.read())

            return response
    else:
        form = ProfileSearchForm()

    return render(request, 'index.html', {'form': form})