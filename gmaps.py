import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAZ0UcwsMV6FchqQhNp--D9ZXEc6onzPNI')


def get_geocode(address):
    return gmaps.geocode(address)

def get_state(geocode_result):
    components = geocode_result[0]["address_components"]
    state = ""
    for names in components:
        potential_state = names["short_name"]
        if len(potential_state) == 2 and potential_state != "US":
            state = potential_state
    return state

#takes in two address strings, returns distance in meters
def get_distance(hospital_one, hospital_two):
    dist_matrix = gmaps.distance_matrix(hospital_one, hospital_two)
    if dist_matrix["status"] == "OK":
        return dist_matrix["rows"][0]["elements"][0]["distance"]['value']
    else:
        return -10 ** 10

# testing
# print(get_distance("368 Broadway, New York, NY 10013", "30 Rockefeller Plaza"))
# print(get_state(geocode_result))
# print(geocode_result[0]["address_components"])
# print(geocode_result[0]["address_components"][2]["short_name"])
