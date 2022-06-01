import websocket,yaml,json,platform,cq_decode,os,datetime

def main():
    print("Your System Type is: {}".format(platform.system()))
    if platform.system() == "Windows":#检测系统 若为WIndows自动退出
        #Windows下不支持将slk转换为除mp3之外的其他格式
        #我懒得弄 直接不允许运行！~
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
        print("Please edit config.yml and run again.")#创建配置文件
        os.system("vim config.yml")
        exit()#没有配置文件就退出
    #开导(指导入配置文件)
    host = config_y['listen'][0]['host']
    port = config_y['listen'][1]['port']
    access_token = config_y['listen'][2]['access_token']
    sufferer = config_y['listen'][3]['sufferer']
    gocq_path = config_y['listen'][4]['gocq_path']
    if os.path.exists(gocq_path) == False:
        print("Go-CQhttp Path not found!")
        print("Please edit config.yml and run again.")
        exit()
    elif os.path.exists(gocq_path + "/data/voices") == False:
        print("Voices folder not found!")#检测音频文件夹是否存在
        print("Please edit config.yml and run again.")
        exit()
    voice_path = config_y['listen'][5]['voice_path']
    if os.path.exists(voice_path) == False:#检测音频保存文件夹是否存在
        os.mkdir(voice_path)#不存在就创建
    voice_name = config_y['listen'][6]['voice_Name']
    url = "ws://{}:{}".format(host, port)
    if access_token is not None:#检测access_token是否为空
        url += "?access_token={}".format(access_token)#不为空就加上
    try:
        ws = websocket.create_connection(url)#连接
    except ConnectionRefusedError:#连接失败
        print("Error: Connection failed.\nPlease check the config file.\nws://{}:{}?access_token={}\nExiting...".format(host,port,access_token))
        exit()
    except websocket._exceptions.WebSocketBadStatusException: #连接失败,这种情况一般都是401,说明access_token错误
        print("Error: Token verification failed.\nPlease check the config file.\nws://{}:{}?access_token={}\nExiting...".format(host,port,access_token))
        exit()
    print("Connected to websocket.Use Ctrl+C to exit.")
    def voice_nformat(voice_name,id):
        output = voice_name.replace('^id^', id).replace('^date^', datetime.datetime.now().strftime("%Y-%m-%d")).replace('^time^', datetime.datetime.now().strftime("%H:%M:%S"))
        #其他我用不上 自己弄啦！！
        return output

    while True:#循环
        try:
            repJson = json.loads(ws.recv())#接收，解析
            if ("message_type" in repJson):#检测是否为消息
                if repJson['user_id'] == sufferer:#检测是否为受害者
                    if repJson['message'][0:16] == "[CQ:record,file=":#检测是否为语音
                        voiceJ = cq_decode.decode(repJson['message'])#解析语音
                        today = str(datetime.date.today())#获取今天日期
                        if os.path.exists(voice_path + "/" + today) == False:#检测今天日期文件夹是否存在
                            os.mkdir(voice_path + "/" + today)#不存在就创建
                            os.mkdir(voice_path + "/" + today + '/slk')#创建slk文件夹
                            os.mkdir(voice_path + "/" + today + '/wav')#创建wav文件夹
                            os.mkdir(voice_path + "/" + today + '/mp3')#创建mp3文件夹
                            os.mkdir(voice_path + "/" + today + '/ogg')#创建ogg文件夹
                        id = str(len(os.listdir(voice_path + "/" + today + '/slk')) + 1).zfill(3)#获取id，并补齐3位
                        os.system("cp {} {}/{}".format(gocq_path + "/data/voices/" +voiceJ['file'], voice_path + '/' + today +"/slk/", voice_nformat(voice_name,id)))#复制语音文件到slk文件夹
                        os.system("sh {}/silk-v3-decoder/converter.sh {} {}".format(os.getcwd(),voice_path + "/" + today + "/slk/" + voice_nformat(voice_name,id), "wav"))#转换语音为wav
                        os.system("sh {}/silk-v3-decoder/converter.sh {} {}".format(os.getcwd(),voice_path + "/" + today + "/slk/" + voice_nformat(voice_name,id), "mp3"))#以下同上
                        os.system("sh {}/silk-v3-decoder/converter.sh {} {}".format(os.getcwd(),voice_path + "/" + today + "/slk/" + voice_nformat(voice_name,id), "ogg"))
                        os.system("mv {} {}".format(voice_path + "/" + today + "/slk/" + voice_nformat(voice_name,id) + ".wav", voice_path + "/" + today + "/wav"))
                        os.system("mv {} {}".format(voice_path + "/" + today + "/slk/" + voice_nformat(voice_name,id) + ".mp3", voice_path + "/" + today + "/mp3"))
                        os.system("mv {} {}".format(voice_path + "/" + today + "/slk/" + voice_nformat(voice_name,id) + ".ogg", voice_path + "/" + today + "/ogg"))
                        print("{}({}) has been saved.".format(voice_nformat(voice_name,id), voiceJ['file']))#打印信息
        except KeyboardInterrupt:#捕获Ctrl+C
            print("Program terminated.")#结束
            exit()#退出
#        except:
#            print("Error: Unknown error.")
#            exit()

if __name__ == "__main__":#主函数
    main()
else:
    print("Error: This file is not supposed to be imported.")
    exit()