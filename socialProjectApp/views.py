from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from socialProjectApp.forms import ProfileSearchForm

# Create a DataFrame for your provided data
data = [
    {"profile pic": 1, "nums/length username": 16, "fullname words": 0, "nums/length fullname": 0,
     "name==username": 0, "description length": 26, "external URL": 0, "private": 1, "#posts": 2,
     "#followers": 271, "#follows": 376, "fake": 0},
    {"profile pic": 0, "nums/length username": 9, "fullname words": 0, "nums/length fullname": 0,
     "name==username": 0, "description length": 0, "external URL": 0, "private": 0, "#posts": 0,
     "#followers": 0, "#follows": 5, "fake": 1},
    # Add more data rows here...
]

# Create a DataFrame from the provided data
df = pd.DataFrame(data)

# Define features (external URL) and labels (fake)
X = df[['external URL']]
y = df['fake']

# Create a Random Forest Classifier
clf = RandomForestClassifier(random_state=42)

# Train the model
clf.fit(X, y)

def predict_fake_account(request):
    if request.method == 'POST':
        form = ProfileSearchForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            parsed_url = urlparse(url)

            if parsed_url.scheme and parsed_url.netloc:  # Check if the URL is valid
                try:
                    # Fetch HTML content from the URL
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract additional features (customize this based on the target website)
                    # Example: Extracting the number of posts from an imaginary website
                    posts_on_website = len(soup.find_all('div', class_='post'))

                    # Make prediction based on extracted features
                    user_input = [[posts_on_website]]  # Provide only the 'posts_on_website' feature
                    prediction = clf.predict(user_input)[0]

                    return render(request, 'result.html', {'prediction': prediction})
                except Exception as e:
                    return HttpResponse(f'An error occurred: {str(e)}')
            else:
                return HttpResponse('Please enter a valid URL.')

    else:
        form = ProfileSearchForm()

    return render(request, 'index.html', {'form': form})
