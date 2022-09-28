import json
import requests
from PyTado.interface import Tado

t = Tado('*******', '******')

def turn_off_heating(id, name):
    print ("Deleting Overlay")
    t.resetZoneOverlay(id)
    telegram_bot_sendtext(f"Resetting_Temperature_for_{name}")

def home_automation():
    zones = t.getZones()
    for zone in zones:
        print(zone["name"])
        if (zone["type"]=="HEATING"):
            state = t.getState(zone["id"])
            if(state["overlay"]):
                print ("**********************")
                if(state["overlay"]["termination"]):
                    print ("****&&&&&&&&&&&&&")
                    if(state["overlay"]["termination"]["type"]=="TIMER"):
                        time_remaining = state["overlay"]["termination"]["remainingTimeInSeconds"]
                        print ("000000000000000000")
                        if (time_remaining > 900):
                            turn_off_heating(zone["id"], zone["name"])
                    elif (state["overlay"]["termination"]["type"]=="MANUAL"):
                        projected_expirty = state["overlay"]["termination"]["projectedExpiry"];
                        print ("1111111111111111")
                        if projected_expirty is None:
                            turn_off_heating(zone["id"], zone["name"])

def telegram_bot_sendtext(bot_message):

   bot_token = '**********'                
   bot_chatID = '5043633097'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   print (send_text)
   response = requests.get(send_text, verify=False)

   return response

def lambda_handler(event, context):
    home_automation()
    return {
        'statusCode': 200,
        'body': json.dumps('Completed running home automation scripts.')
    }

if __name__ == "__main__":
    home_automation()
