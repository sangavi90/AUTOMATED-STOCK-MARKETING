import geocoder

def geolocate_ip(ip_address):
    g = geocoder.ip(ip_address)
    if g.ok:
        return g.json
    else:
        return None

ip_address = "2409:4071:4d35:6a5f:f6f7:a75a:246b:eb5c"  # Example IP address
location = geolocate_ip(ip_address)
print(location)