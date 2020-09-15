import requests
import json
from pprint import pprint

def search_location( location ):

    radius=1

    #보증금
    deposit_s=0
    deposit_e=10000

    #월세
    rent_s=0
    rent_e=40

    #층수
    floor="1~|rooftop|semibase"

    #지하철역( 수유역 )
    subway_id=96

    url = f'https://apis.zigbang.com/v3/items/ad/{subway_id}?subway_id={subway_id}&radius={radius}&sales_type=&deposit_s={deposit_s}&deposit_e={deposit_e}&rent_s={rent_s}&rent_e={rent_e}&floor={floor}&domain=zigbang&detail=false'

    req = requests.get(url)

    if req.status_code == 200:
        data = json.loads( req.text )

        if data["success"] == True:
            items = data["items"]

            for item in items:
                desc = {
                    "location": item["description"]
                    , "type": ( item["type"], item["hint"], item["id"] )
                    , "pos": {
                        "lat": item["lat"]
                        , "lng": item["lng"]
                    }
                    , "zoom": {
                        "level": item["zoom"]
                        , "daum": item["zoom_level"]["daum"]
                        , "google": item["zoom_level"]["google"]
                        , "app": item["zoom_level_v2"]["app"]
                        , "web": item["zoom_level_v2"]["web"]
                    }
                }

                pprint( desc )


'''

https://apis.zigbang.com/v3/items2?lat_south=33.64246368408203&lat_north=33.64246368408203&lng_west=111.0220947265625&lng_east=111.0220947265625&need_more_zoom_in=false
https://www.zigbang.com/home/oneroom/items?lat_south=33.64246368408203&lat_north=33.64246368408203&lng_west=111.0220947265625&lng_east=111.0220947265625&need_more_zoom_in=false
https://www.zigbang.com/home/oneroom/items?lat_south=37.64246368408203&lat_north=37.64246368408203&lng_west=127.0220947265625&lng_east=127.0220947265625&need_more_zoom_in=false
https://www.zigbang.com/home/oneroom/items?lat_south=37.65131759643555&lat_north=37.65131759643555&lng_west=127.02919006347656&lng_east=127.02919006347656&need_more_zoom_in=false

url = 'https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash=wydq4&rent_gteq=0&sales_type_in={}&service_type_eq={}'.format('전세|월세', '원룸')

보증금
deposit_s=0 - 시작
deposit_e=10000 - 끝

월세
rent_s=0 - 시작
rent_e=40 - 끝

층수
floor=1~%7Crooftop%7Csemibase

domain=zigbang&detail=false

지하철역( 수유역 )
subway_id=96

https://apis.zigbang.com/v3/items/ad/96?subway_id=96&radius=1&sales_type=&deposit_s=0&rent_s=0&floor=1~%7Crooftop%7Csemibase&domain=zigbang&detail=false
https://apis.zigbang.com/v3/items/ad/96?subway_id=96&radius=1&sales_type=&deposit_s=0&rent_s=0&floor=1~%7Crooftop%7Csemibase&domain=zigbang&detail=false

f'https://apis.zigbang.com/v3/items/ad/96?subway_id=96&radius=1&sales_type=&deposit_s={deposit_s}&deposit_e=10000&rent_s=0&rent_e=40&floor=1~%7Crooftop%7Csemibase&domain=zigbang&detail=false'
https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash=wydq6&rent_gteq=0&sales_type_in=%EC%A0%84%EC%84%B8%7C%EC%9B%94%EC%84%B8&service_type_eq=%EC%9B%90%EB%A3%B8
https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash=wydq1&rent_gteq=0&sales_type_in=%EC%A0%84%EC%84%B8%7C%EC%9B%94%EC%84%B8&service_type_eq=%EC%9B%90%EB%A3%B8
https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash=wydq5&rent_gteq=0&sales_type_in=%EC%A0%84%EC%84%B8%7C%EC%9B%94%EC%84%B8&service_type_eq=%EC%9B%90%EB%A3%B8
https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash=wydq4&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸
'''