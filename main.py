import websocket
import yaml
import json
import platform
import cq_decode
import os
import datetime
#{"anonymous":null,"font":0,"group_id":365697768,"message":"[CQ:record,file=17670CF0648AC14455D8B8101F4C6003.amr,url=http://grouptalk.c2c.qq.com/?ver=0\u0026amp;rkey=3062020101045b30590201010201010204073dd4dd042439386a4f467248346563696730444f35444e305941466f4d346c355355324e3763315330020462956dbb041f0000000866696c6574797065000000013100000005636f64656300000001310400\u0026amp;filetype=1\u0026amp;voice_codec=1]","message_id":-217799010,"message_seq":7153,"message_type":"group","post_type":"message","raw_message":"[CQ:record,file=17670CF0648AC14455D8B8101F4C6003.amr]","self_id":121492701,"sender":{"age":0,"area":"","card":"","level":"","nickname":"Vm#262","role":"admin","sex":"unknown","title":"","user_id":591511593},"sub_type":"normal","time":1653960123,"user_id":591511593}
def main():
    print("Your System Type is: {}".format(platform.system()))
    if platform.system() == "Windows":
        print("Windows is not supported!")
        exit()
    try:#try to import the config file
        config_f = open(r'config.yml')
        config_y = yaml.load(config_f, Loader=yaml.FullLoader)
    except IOError:#if no have config.tml
        config_f = open('config.yml', 'w')
        config_f.write("""listen:
    - host: localhost
    - port: 6700
    - access_token: ''
    - sufferer: 114514
    - gocq_path: /home/username/cq_bot/
    - voice_path: /path/to/file
    - voice_Name: vm^id^""")
        print("No config.yml file found.") 
        print("Please edit config.yml and run again.")
        exit()
    host = config_y['listen'][0]['host']
    port = config_y['listen'][1]['port']
    access_token = config_y['listen'][2]['access_token']
    sufferer = config_y['listen'][3]['sufferer']
    gocq_path = config_y['listen'][4]['path']
    if os.path.exists(gocq_path) == False:
        print("Go-CQhttp Path not found!")
        print("Please edit config.yml and run again.")
        exit()
    elif os.path.exists(gocq_path + "/go-cqhttp") == False:
        print("Go-CQhttp not found!")
        print("Please edit config.yml and run again.")
        exit()
    voice_path = config_y['listen'][5]['path']
    if os.path.exists(voice_path) == False:
        os.mkdir(voice_path)
    voice_name = config_y['listen'][6]['voice_name']
    url = "ws://{}:{}".format(host, port)
    if access_token is not None:
        url += "?access_token={}".format(access_token)
    try:
        ws = websocket.create_connection(url)
    except ConnectionRefusedError:
        print("Error: Connection failed.\nPlease check the config file.\nws://{}:{}?access_token={}\nExiting...".format(host,port,access_token))
    print("Connected to websocket.Use Ctrl+C to exit.")
    def voice_nformat(voice_name,id):
        output = voice_name.replace('^id^', '{}').format(id)
        return output

    while True:
        try:
            repJson = json.loads(ws.recv())
            if ("message_type" in repJson):
                if repJson['user_id'] == sufferer:
                    if repJson['message'][0:1] == "[CQ:record,file=":
                        voiceJ = cq_decode.decode(repJson['message'])
                        if os.path.exists(voice_path + "/" + datetime.date.today()):
                            os.mkdir(voice_path + "/" + datetime.date.today() + 'slk')
                            os.mkdir(voice_path + "/" + datetime.date.today() + 'wav')
                            os.mkdir(voice_path + "/" + datetime.date.today() + 'mp3')
                            os.mkdir(voice_path + "/" + datetime.date.today() + 'ogg')
                    id = len(os.listdir(voice_path + "/" + datetime.date.today() + 'slk','r')) + 1
                    os.system("cp {} {}/{}".format(gocq_path + "/data/voice/" + voiceJ['file'], voice_path + "/slk" + datetime.date.today(), voice_nformat(voice_name,id)))
                    os.system("sh silk-v3-decoder.sh {} {} {}".format(voice_path + "/" + datetime.date.today() + "/slk/" + voice_nformat(voice_name,id), voice_path + "/" + datetime.date.today() + "/wav/" + voice_nformat(voice_name,id) + ".wav", 'wav'))
                    os.system("sh silk-v3-decoder.sh {} {} {}".format(voice_path + "/" + datetime.date.today() + "/slk/" + voice_nformat(voice_name,id), voice_path + "/" + datetime.date.today() + "/mp3/" + voice_nformat(voice_name,id) + ".mp3", 'mp3'))
                    os.system("sh silk-v3-decoder.sh {} {} {}".format(voice_path + "/" + datetime.date.today() + "/slk/" + voice_nformat(voice_name,id), voice_path + "/" + datetime.date.today() + "/ogg/" + voice_nformat(voice_name,id) + ".ogg", 'ogg'))
                    print("{}({}) has been saved.".format(voice_nformat(voice_name,id), voiceJ['file']))
        except KeyboardInterrupt:
            print("Program terminated.")
            exit()
#        except:
#            print("Error: Unknown error.")
#            exit()

if __name__ == "__main__":
    main()