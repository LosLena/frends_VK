import time
import requests
from pprint import pprint
from urllib.parse import urlencode

my_token = "1f21b419dc27e379227fab3b905d21f3a74f46aa143e64894369b15703b6f555b75c3013a6cd23a07955d"
requests_url = "https://api.vk.com/method/"
# Процедура получения токена
def get_token():
  id = 7405393
  oauth_url = 'https://oauth.vk.com/authorize'
  oauth_params ={
  'client_id': id,
  'display': 'page',
  'response_type': 'token',
  'scope': "friends, status, wall, groups, stats, offline",
  'v': '5.103'}
  print("?".join((oauth_url, urlencode(oauth_params))))
  
#get_token()


class FrendsVK:
    def __init__(self, user_id):
        self.user_id = user_id
        self.params = {
            "access_token": my_token,
            "v": "5.103",
            "user_ids": self.user_id,}
   
    def get_name(self):
        method = "users.get"
        response = requests.get(requests_url + method, self.params)
        data = response.json()
        #print(data)
        self.account_id = data['response'][0]['id'] 
        name = " ".join((data['response'][0]['first_name'],data['response'][0]['last_name']))
        #print(name)
        return name


    def get_friends_list(self):
        method = "friends.get"
        #self.params["count"] = 5000
        self.params["user_id"] = self.account_id
        response = requests.get(requests_url + method, self.params)
        data = response.json()
        #print((data['response']['items'])
        return data['response']['items']

    def __and__(self, other):
        me = self.get_friends_list()
        frend = other.get_friends_list()
        set_me = set(me)
        set_friend = set(frend)
        common_friends = set_me & set_friend
        common_friends_dict = {}
        common_friends_list = []
        for friend in common_friends:
            common_friends_list.append(FrendsVK(friend)) 
            name = FrendsVK(friend).get_name()
            common_friends_dict[name] = {'id': friend, 'url': 'https://vk.com/id' + str(friend)}
        print(" Количество обших друзей".format(len(common_friends_list)))
        for item in common_friends_list:
            print("{} <-> cсылка на профиль: {}".format(item.get_name(), common_friends_dict[item.get_name()]['url']))




#response = requests.get(requests_url+'status.get', 
#params={'access_token': my_token,'v': 5.103}) 

#print(response.json())      
Me = FrendsVK(259482275)
Frend = FrendsVK(110969138) 
#Me.get_name()
#Frend.get_name()
print(f"У пользователя {Me.get_name()}  количество друзей {len(Me.get_friends_list())}")
print(f"У пользователя {Frend.get_name()}  количество друзей {len(Frend.get_friends_list())}")

Me&Frend