import socket

def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to a remote server (doesn't matter which one)
        s.connect(("8.8.8.8", 80))
        
        # Get the local IP address
        local_ip = s.getsockname()[0]
        
        # Close the socket
        s.close()
        
        return local_ip
    except Exception as e:
        print("Error occurred while retrieving local IP:", e)
        return None

# Call the function to get the local IP address
local_ip = get_local_ip()

if local_ip:
    print("Local IP address:", local_ip)
else:
    print("Failed to retrieve local IP address.")
