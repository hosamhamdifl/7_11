import scrapy
import json
import pandas as pd
import requests


class Spider711Spider(scrapy.Spider):
    name = "spider_7_11"
    allowed_domains = ["apis.7-eleven.com"]
    #start_urls = ["https://www.7-eleven.com/locator","https://apis.7-eleven.com/v5/stores/graphql"]


# URL for the API
url = "https://apis.7-eleven.com/v5/stores/graphql"

# Headers (include cookies and authorization)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzbDNyZ2RVNWM1WnZzWWo5NUZHSXVleGF1NU50N0o1T1RmN1ZSUGZWIiwic2NvcGUiOiJyZWFkX3N0b3JlcyByZWFkX2NvbmZpZyByZXNldF9wYXNzd29yZCBlbWFpbF9zdWJzY3JpcHRpb25zIGNvbXBsaWFuY2VfcmVxdWVzdCIsImdyYW50X3R5cGUiOiJjbGllbnRfY3JlZGVudGlhbCIsImV4cCI6MTczNDcxNjI4OCwiaWF0IjoxNzM0NjI5ODg4fQ.lJJ_uhoYKc3_JXWRJMr8fxMXx_vecJP3SqLP8Y78odrMiY--58o88kqNtqN9X--tFHmBwhQMEAjbwZBGBv_13s8fpMtoQscbbaHNRi_4bMREIXNamYnsMfMUb8EvcZdU9_zunwIoYWQR56ts0rE8C1OpkCvwMIKS7yzPd1TkHC-w1C4_5tQyV3ATcBY0_5tgQsAvGNA-alsxJRzTWIY6r5pZ9jnbrZcyFa-vakyF61khQ2de7VVW6_d726Z0mc_2EwAaKbO3D2ii1D0Tnu4QJyJSJZsFkdxrmEoLYznuxO-zts6yp7mB9_bGABUs-n_hT2Qp4uccRzAAWDw-W0gsSQ",
    "Cookie": "csrftoken=ThKgQgydBGGeEmI8vKTknYqWoLzJBjxK7KgsI1FpONK2enozLj4xmF3cTvbwryF1"
}

# Payload for the POST request
payload = {
    "operationName": "stores",
    "variables": {
        "lat": "35.7595731",
        "lon": "-79.01929969999999",
        "radius": 450,
        "limit":  10000,
        "curr_lat": "35.7595731",
        "curr_lon": "-79.01929969999999",
        "filters": []
    },
    "query": """
    query stores($lat: String, $lon: String, $radius: Float, $limit: Int, $curr_lat: String, $curr_lon: String, $filters: [String]) {
      stores(
        lat: $lat
        lon: $lon
        radius: $radius
        limit: $limit
        curr_lat: $curr_lat
        curr_lon: $curr_lon
        filters: $filters
      ) {
        address
        brand {
          slug
          logo
        }
        distance_label
        distance
        lat
        lon
        hours
        id
        name
        city
        phone
        state
        country
        postal_code
        franchise
        features {
          slug
          title
        }
        services {
          slug
          title
        }
        local_content
        fuel_data
        local_images
      }
    }
    """
}

# Send POST request
response = requests.post(url, json=payload, headers=headers)

# Check response status
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
    data = response.json()
    stores = data.get("data", {}).get("stores", [])
    store_list = [
        {
            "Name": store.get("name"),
            "Address": store.get("address"),
            "City": store.get("city"),
            "State": store.get("state"),
            "Postal Code": store.get("postal_code"),
            "Phone": store.get("phone"),
            "Latitude": store.get("lat"),
            "Longitude": store.get("lon"),
            "Distance": store.get("distance"),
            "Brand": store.get("brand", {}).get("slug") if store and store.get("brand") and store.get("brand").get("slug") is not None else "Unknown",
            "Hours": store.get("hours"),
        }
        for store in stores if store and store.get("state") == "NC"
    ]
    df = pd.DataFrame(store_list)

    # Save to an Excel file
    output_file = "7eleven_stores.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)


    def parse(self, response):
      pass