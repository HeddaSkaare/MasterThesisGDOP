
import requests
from requests.auth import HTTPBasicAuth
import os
import gzip
import shutil

# # Print the parsed ephemerides

base_url = "https://cddis.nasa.gov/archive/gnss/data/daily/2024/brdc/"

# Earthdata credentials (replace with your own)
username = "heddsk"
password = "k!@*J$x67NMSyfj"

# The specific file you want to download (e.g., broadcast ephemerides)
daynumber = "269"
filename = f"BRDC00IGS_R_2024{daynumber}0000_01D_MN.rnx.gz"
file_url = base_url + filename

session = requests.Session()
session.auth = HTTPBasicAuth(username, password)

# Make the request with the session (this will follow redirects properly)
response = session.get(file_url)

# Check if the response indicates a successful download
if response.headers.get('Content-Type') != 'application/x-gzip':
    print("Error: The downloaded file is not a gzipped file.")
    print(f"Response content type: {response.headers.get('Content-Type')}")
    print("Response text (first 200 characters):", response.text[:200])
else:
    # Save the .gz file locally if it's valid
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded: {filename}")

    # Step 4: Decompress the .gz file to .rnx file
    unzipped_filename = filename[:-3]  # Remove '.gz' from filename
    with gzip.open(filename, 'rb') as f_in:
        with open(unzipped_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Decompressed: {unzipped_filename}")
