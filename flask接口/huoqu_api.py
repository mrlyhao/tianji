import requests

for i in range(5):
    url='http://39.104.62.136:****/get_user?url=http://www.qichacha.com/firm_g13634b6b44b386c0c7b7fca310c36e9.html'
    # headers={'username':'huhy'}
    a=requests.get(url).text
    print(a)