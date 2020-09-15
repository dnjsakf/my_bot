import telepot
from zigbang import find_room
import json

TELEPOT_TOKEN = '906438431:AAEMIf7jB9jTTx3DPdezoMVAh1jBpBCf0AA'

found_room_info = list()
last_send_index = 0

def send_room_info( chat_id, room_info ):
    bot.sendMessage( chat_id, room_info["url"] )
    bot.sendMessage( chat_id, room_info["제목"] )
    bot.sendMessage( chat_id, room_info["설명"]["description"] )
    bot.sendMessage( chat_id, '{}, {}, {}'.format( room_info["정보"]["전세/월세"], room_info["정보"]["층수"], room_info["정보"]["방"] ) )
    bot.sendMessage( chat_id, '관리비: {}, 보증금액: {}, 월세금액: {}'.format( room_info["비용"]["관리비"], room_info["비용"]["보증금액"], room_info["비용"]["월세금액"] ) )
    bot.sendMessage( chat_id, "="*30 )

def handler( msg ):
    global found_room_info
    global last_send_index

    content_type, chat_Type, chat_id, msg_date, msg_id = telepot.glance( msg, long=True )

    print( content_type, chat_Type, chat_id, msg_date, msg_id )
    print( msg )
    
    recieved = msg["text"].split(" ")

    if recieved[0] == "/find":
        bot.sendMessage( chat_id, '찾는중...' )
        
        found_room_info = find_room( recieved[-1] )

        bot.sendMessage( chat_id, '{}개의 방을 찾았습니다.'.format( len(found_room_info) ) )

        if len(found_room_info) > 0:
            last_send_index = 0
            send_room_info( chat_id, found_room_info[last_send_index] )

    elif recieved[0] == "/more":
        if len(found_room_info) >= last_send_index + 1:
            last_send_index += 1
            send_room_info( chat_id, found_room_info[last_send_index] )
        

bot = telepot.Bot( TELEPOT_TOKEN )
bot.message_loop( handler, run_forever=True )