import json

#将CQ码转换为JSON
#十分简单 小学生都会做~
def decode(cq_str):
    cq_str = cq_str[1 : len(cq_str) - 1].split(',')#去除中括号,并以逗号分隔
    cq_str[0] = cq_str[0].replace('CQ:', 'CQ=')#替换CQ:
    for i in range(len(cq_str)):
        cq_str[i] = cq_str[i].replace('=', '":"' , 1)#替换=为":" 每个项目只替换一次
        cq_str[i] = '"' + cq_str[i] + '"'#添加双引号
    cq_str = '{' + ','.join(cq_str) + '}'#添加花括号
    return json.loads(cq_str)#转换为JSON后返回

if __name__ == "__main__": #测试
    print("使用方法: cq_decode.decode(cq_str)")
    print("例如: cq_decode.decode('[CQ:record,file=17670CF0648AC14455D8B8101F4C6003.amr]')")
    print("输出:" + decode('[CQ:record,file=17670CF0648AC14455D8B8101F4C6003.amr]'))
