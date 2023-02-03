import json
import requests

# Read "wkda" from marke.json
with open('marke.json') as f:
    data = json.load(f)
    wkda = data["https://api-mcj.wkda.de/v1/cardata/types/manufacturers-{\"locale\":\"de-DE\",\"country\":\"de\"}"]["response"]["result"]["wkda"]

# Loop throught all key and value pairs

marke_modelle = []

for key, value in wkda.items():
    # Send request like https://api-mcj.wkda.de/v1/cardata/types/main-types?manufacturer=107&locale=de-DE&country=de where 107 is the key
    url = "https://api-mcj.wkda.de/v1/cardata/types/main-types?manufacturer=" + key + "&locale=de-DE&country=de"
    response = requests.get(url)
    modelle = response.json()

    append = {
        "marke": {
            key : value,
            "modelle" : modelle["wkda"],
        },
    }


