import math
import requests
from PIL import Image
from requests.auth import HTTPBasicAuth
import os
import json
from io import BytesIO


class PlanetDownloader:
    def __init__(self, api_key, item_type='PSScene3Band'):
        self.api_key = api_key
        self.item_type = item_type
    
    def create_cords(lat, lon):
        amt = 0.0005
        lat_down = lat - amt*10
        lat_up = lat + amt*10

        lon_left = lon - amt/10
        lon_right = lon + amt/10

        return [[lon_left, lat_down], [lon_right, lat_down], [lon_right, lat_up], [lon_left, lat_up]]
    
    
    def deg_to_tile(lat_deg, lon_deg, zoom):
        """Converts coordinates into the nearest x,y Slippy Map tile"""
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad)))
                     / math.pi) / 2.0 * n)
        return (xtile, ytile)
        
    def download_image(self, lat, lon, min_year, min_month, max_year, max_month, zoom=14):
        if min_month < 10:
            min_month = '0' + str(min_month)

        if max_month < 10:
            max_month = '0' + str(max_month)
        
        geo_json_geometry = {
          "type": "Polygon",
          "coordinates": [
              PlanetDownloader.create_cords(lat, lon)
          ],

        }

        # filter for items the overlap with our chosen geometry
        geometry_filter = {
          "type": "GeometryFilter",
          "field_name": "geometry",
          "config": geo_json_geometry,
        }

        # filter images acquired in a certain date range
        date_range_filter = {
          "type": "DateRangeFilter",
          "field_name": "acquired",
          "config": {
            "gte": "{}-{}-01T00:00:00.000Z".format(min_year, min_month),
            "lte": "{}-{}-01T00:00:00.000Z".format(max_year, max_month)
          }
        }

        # filter any images which are more than 50% clouds
        cloud_cover_filter = {
          "type": "RangeFilter",
          "field_name": "cloud_cover",
          "config": {
            "lte": 0.2
          }
        }

        # create a filter that combines our geo and date filters
        # could also use an "OrFilter"
        reservoir = {
          "type": "AndFilter",
          "config": [geometry_filter, date_range_filter, cloud_cover_filter]
        }
        
        # Search API request object
        search_endpoint_request = {
          "item_types": [self.item_type],
          "filter": reservoir
        }

        result = \
          requests.post(
            'https://api.planet.com/data/v1/quick-search',
            auth=HTTPBasicAuth(self.api_key, ''),
            json=search_endpoint_request)
        
        res = json.loads(result.text)
        item_id = None

        if len(res['features']) == 0:
            print('No image found, try widening your search or using a different satellite')
            return
        else:
            # choose middle idx
            idx = len(res['features']) // 2
            item_id = res['features'][idx]['id']
            
            
        x, y = PlanetDownloader.deg_to_tile(lat, lon, zoom)
        url = 'https://tiles0.planet.com/data/v1/{}/{}/{}/{}/{}.png?api_key={}'.format(self.item_type, item_id, zoom, x, y, self.api_key)
        
        res = requests.get(url)
        if res.status_code >= 400:
            print('download error')
            return
        
        return Image.open(BytesIO(res.content))

       