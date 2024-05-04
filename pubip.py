import requests

def get_public_ip():
    try:
        # Make a GET request to a public IP address lookup service
        response = requests.get('https://api.ipify.org')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract and return the public IP address from the response
            return response.text
        else:
            print("Failed to retrieve public IP address. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error occurred while retrieving public IP address:", e)
        return None

# Call the function to get the public IP address
public_ip = get_public_ip()

if public_ip:
    print("Public IP address:", public_ip)
else:
    print("Failed to retrieve public IP address.")
