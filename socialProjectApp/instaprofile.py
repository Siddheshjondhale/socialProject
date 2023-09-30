import instaloader

# Creating an Instaloader() object
ig = instaloader.Instaloader()

# Taking the Instagram username as input from the user
username = input("Enter username: ")

# Fetching the details of the provided username using Instaloader object
profile = instaloader.Profile.from_username(ig.context, username)

# Printing the fetched details
print("Username:", profile.username)
print("Number of Posts Uploaded:", profile.mediacount)
print(profile.username + " is having " + str(profile.followers) + ' followers.')
print(profile.username + " is following " + str(profile.followees) + ' people')
print("Bio:", profile.biography)

# Download the profile picture (profile photo) using Instaloader
ig.download_profile(username, profile_pic_only=True)
