from geopy import geocoders

resolved_locations = {}

def geodecode(location):
    # check if location already resolved
    if location in resolved_locations:
        loc = resolved_locations.get(location, "none")
    else:
        g = geocoders.Nominatim(user_agent="dummy")
        loc = g.geocode(location, timeout=10)
        # store location and coord
        resolved_locations[location] = loc

    return loc.latitude, loc.longitude