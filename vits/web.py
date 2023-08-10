import requests
import json
import jsonpath
import urllib

def sendprompt(prompt: str):

    payload = {
        "prompt":"",
        "cdn":"true"
    }
    payload["prompt"]=prompt
    url = "http://localhost:5000/api/send_and_receive"

    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

    print(response.json())
    dic=response.json()
    u=jsonpath.jsonpath(dic,"$..latest_image_url")
    print(u)
    last=str(u[0])
    last=last[last.rfind('/')+1:len(last)]
    return last,u[0]
def upscale(pic:str,target:int):
    base_url = 'http://localhost:5000'  # 替换为您的 Flask 应用实际运行的 URL
    file_name = pic  # 替换为您的实际文件名
    number = target  # 替换为您想要使用的数字

    response = requests.get(f'{base_url}/upscale', params={'file_name': file_name, 'number': number})

    if response.status_code == 200:
        print('Success!')
        print(response.json())
        dic=response.json()
        u=jsonpath.jsonpath(dic,"$..latest_image_url")
        print(u)
        return u[0]
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return ''
# sendprompt("a girl")
# urllib.request.urlretrieve(url='https://cdn.discordapp.com/attachments/1116936643773997179/1117329588247347221/timothydavis_a_girl_1e94bd97-5159-49b6-b784-69be2ab29a15.png',filename='./mid.png')