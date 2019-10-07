import requests
from pprint import pprint
import time
import json
access_token = '113b717a9bcc61855524bb35c03f681849b243d21004a64cab6b256b037df8c32611124e452336e0459ed'


class User:
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id
        self.url = f'https://vk.com/id{self.user_id}'

    def get_params(self):
        return {
            'user_id': self.user_id,
            'access_token': self.access_token,
            'v': 5.101
        }

    def get_friends(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params=params
        )
        return response.json()

    def get_groups(self, user_id):
        params = {
            'user_id': user_id,
            'access_token': self.access_token,
            'extended': 0,
            'v': 5.101
        }
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params=params
        )
        return response.json()

    def onli_you_group(self, groups, friends):
        groups_friends = set()
        counter = 0
        friends_counter = 0
        counter_private = 0
        print(f'У пользователя всего {friends["response"]["count"]} друзей ')
        for i in friends['response']['items']:
            friends_counter += 1
            print(f'Обрабатано {friends_counter} из {friends["response"]["count"]} друзей')
            group = self.get_groups(i)
            try:
                groups_friends.update(group['response']['items'])
            except KeyError:
                if group['error']['error_code'] == 30:
                    counter_private += 1
                    continue
                elif group['error']['error_code'] == 6:
                    time.sleep(0.3)
                    friends['response']['items'].append(i)
                    friends_counter -= 1
                    continue
                elif group['error']['error_code'] == 7:
                    counter_private += 1
                    continue
                elif group['error']['error_code'] == 18:
                    counter += 1
                    continue
                else:
                    continue
        print(f'\n\nПрограмме не получилось получить доступ к {counter} пользователям. \n'
              f'Так как их странички удалены или заблокированы \n'
              f'А так же у {counter_private} пользователей приватные страницы')
        you_group = set(groups['response']['items']).difference(groups_friends)
        return you_group

    def info_group(self, group_id):
        params = {
            'group_id': group_id,
            'access_token': self.access_token,
            'fields': 'members_count',
            'extended': 0,
            'v': 5.101
        }
        response = requests.get(
            'https://api.vk.com/method/groups.getById',
            params=params
        )
        group_info = {
            'name': response.json()['response'][0]['name'],
            'git': response.json()['response'][0]['id'],
            'members_count': response.json()['response'][0]['members_count']
        }
        return group_info


def write(file_load):
    with open('/home/mishanya/Python/дз/Diploma/groups.json', mode='w', encoding='utf8') as f:
        json.dump(file_load, f, ensure_ascii=False, indent=2)


def execution():
    user_id = input("Введите id пользователя ")
    user = User(access_token, user_id)
    print('Инициировали пользователя')
    groups = user.get_groups(user_id)
    print("Определили группы в которые входит пользователь")
    friends = user.get_friends()
    print("Нашли друзей пользователя ")
    you_group = user.onli_you_group(groups, friends)
    print("Нашли id групп в которые входит только наш пользователь ")
    file_load = []
    counter_end = len(you_group)
    counter = 0
    for group_id in you_group:
        counter += 1
        print(f'Получаем информацию о {counter} группе из {counter_end}')
        time.sleep(0.3)
        try:
            you_group = user.info_group(group_id)
            file_load.append(you_group)
        except KeyError:
            print(f'Не удалось получить информацию о группе {counter}')
            continue
    print("Вот группы в которых состоит только наш пользователь и никто из его друзей")
    print("Записываем json файл с описанием групп")
    write(file_load)
    print("Записали информацию в groups.json файл проверяйте")


execution()