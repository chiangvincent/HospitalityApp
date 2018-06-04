import googlemaps

gmaps = googlemaps.Client(key='AIzaSyD1WBmCVoRsgtwPB61umBRu9iB-S_LzC7M')


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

#testing
# print(get_state(geocode_result))
# print(geocode_result[0]["address_components"])
# print(geocode_result[0]["address_components"][2]["short_name"])
