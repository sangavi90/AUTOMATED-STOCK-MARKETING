import requests

# Define the API endpoint URL
api_url = 'https://apiconnect.angelbroking.com/data'

# Make a GET request to the API endpoint
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract data from the response
    data = response.json()
    # Process the data as needed
    print(data)
else:
    # Print an error message if the request failed
    print("Failed to retrieve data from the API. Status code:", response.status_code)
