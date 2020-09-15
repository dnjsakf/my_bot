import requests
import json
from pprint import pprint

from celery import Celery, chord

app = Celery('req_celery', broker="amqp://heo:heo@localhost:5672//", backend="amqp://")

def find_subway_info( find_subway=None ):
    url = 'https://apis.zigbang.com/property/biglab/subway/all?'
    
    req = requests.get(url)
    if req.status_code == 200:
        items = json.loads( req.text )

        subway_info = [ (item['id'], item['name']) for item in items if item['name'] == find_subway ]

        if subway_info and len(subway_info) > 0:
            return subway_info[0]

    return (None, None)
    
@app.task
def find_room_info( item_id ):
    room_info = None

    url = f'https://apis.zigbang.com/v2/items/{ item_id }'

    req = requests.get( url )

    if req.status_code == 200:
        data = json.loads( req.text )

        if data["item"].get("description").find( "대출" ) > 0:
            room_info = {
                "url": 'https://www.zigbang.com/home/oneroom/items/{}'.format( data["item"].get("item_id") )
                , "item_id": data["item"].get("item_id")
                , "제목": data["item"].get("title")
                , "주소": ( data["item"].get("local1"), data["item"].get("local2"), data["item"].get("local3"), data["item"].get("local4") )
                , "설명": {
                    "comment": data["item"].get("agent_comment")
                    , "description": data["item"].get("description")
                }
                , "정보": {
                    "사진": data["item"].get("images")
                    , "전세/월세": data["item"].get("sales_type")
                    , "방": data["item"].get("service_type")
                    , "층수": "{}/{}".format( data["item"].get("floor"),  data["item"].get("floor_all") )
                }
                , "비용": {
                    "관리비": data["item"].get("manage_cost")
                    , "보증금액": data["item"].get("보증금액")
                    , "월세금액": data["item"].get("월세금액")
                }
                , "면적": {
                    "공급면적_m2": data["item"].get("공급면적_m2")
                    , "대지권면적_m2": data["item"].get("대지권면적_m2")
                    , "전용면적_m2": data["item"].get("전용면적_m2")
                }
                , "중개사": data["agent"].get("owner")
            }

    return room_info

@app.task
def callback( results ):
    return [ res for res in results if res is not None ]

def find_room( subway_name ):
    #보증금
    deposit_s=0
    deposit_e=10000

    #월세
    rent_s=0
    rent_e=40

    #층수
    floor="1~|rooftop|semibase".replace('|', '%7C')

    #지하철역( 수유역 )
    subway_id, _ = find_subway_info( subway_name )

    #검색반경
    radius=1

    url = f'https://apis.zigbang.com/v3/items/ad/{ subway_id }?subway_id={ subway_id }&radius={ radius }&sales_type=&deposit_s={ deposit_s }&deposit_e={ deposit_e }&rent_s={ rent_s }&rent_e={ rent_e }&floor={ floor }&domain=zigbang&detail=false'

    req = requests.get(url)
    
    tasks = []

    if req.status_code == 200:
        data = json.loads( req.text )

        item_ids = [ item["simple_item"]["item_id"] for item in data["list_items"] if 'ad_agent' not in item ]

        for item_id in item_ids:

            task = find_room_info.s( item_id )

            tasks.append( task )
            
    runner = chord( tasks )

    return runner( callback.s() ).get()
