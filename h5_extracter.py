# Small script that takes all hdf5-files in a folder and extracts various 
# features into a Pandas dataframe
# Written by Linus Jacobsson March 13 2023
# Note! More processing of the feature is needed before deployment

import os
import pandas as pd
import hdf5_getters

# Define a list to store the data
data = []

# Set the directory containing the hdf5 files
dir_path = "/home/ubuntu/songs"

# Get a list of all the hdf5 files in the directory
file_list = [f for f in os.listdir(dir_path) if f.endswith('.h5')]

# Loop over the files and extract the features
for file_name in file_list:
    # Open the hdf5 file
    h5 = hdf5_getters.open_h5_file_read(os.path.join(dir_path, file_name))

    # Extract the features
    artist_familiarity = hdf5_getters.get_artist_familiarity(h5)
    artist_hotttnesss = hdf5_getters.get_artist_hotttnesss(h5)
    artist_id = hdf5_getters.get_artist_id(h5)
    artist_mbid = hdf5_getters.get_artist_mbid(h5)
    artist_playmeid = hdf5_getters.get_artist_playmeid(h5)
    title = hdf5_getters.get_title(h5)
    artist_latitude = hdf5_getters.get_artist_latitude(h5)
    artist_longitude = hdf5_getters.get_artist_longitude(h5)
    artist_name = hdf5_getters.get_artist_name(h5)
    release = hdf5_getters.get_release(h5)
    song_hotttness = hdf5_getters.get_song_hotttnesss(h5)
    danceability = hdf5_getters.get_danceability(h5)
    duration = hdf5_getters.get_duration(h5)
    year = hdf5_getters.get_year(h5)
    

    # Add the features to the data list
    data.append([file_name, artist_familiarity, 
artist_hotttnesss,artist_name \
                                 
,title,artist_latitude,artist_longitude,danceability,duration ,year])

    # Close the hdf5 file
    h5.close()

# Convert the data list to a pandas dataframe
df = pd.DataFrame(data, columns=["file_name", "artist_familiarity", 
"artist_hotttnesss", "artist_name"\
                                 
,"title","artist_latitude","artist_longitude","danceability","duration","year"])

print(df.head(100))
