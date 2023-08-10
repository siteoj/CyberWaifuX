# import requests

# base_url = 'http://localhost:5000'  # 替换为您的 Flask 应用实际运行的 URL
# file_name = 'timothydavis_a_girl_10990004-dff2-40bb-8000-7034ec3b4172.png'  # 替换为您的实际文件名
# number = 3  # 替换为您想要使用的数字

# response = requests.get(f'{base_url}/upscale', params={'file_name': file_name, 'number': number})

# if response.status_code == 200:
#     print('Success!')
#     print(response.json())
# else:
#     print(f'Error: {response.status_code}')
#     print(response.text)