import requests
from pprint import pprint
import time
import json
access_token = '44fd7dff09d5bd32bd898a8b4cb5205066e06a8f49b43c4965ad0382b38977aa9dd8e9fa4c7734a606d57'


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

    def get_groups(self):
        params = {
            'user_id': self.user_id,
            'access_token': self.access_token,
            'extended': 0,
            'v': 5.101
        }
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params=params
        )
        return response.json()


def get_group(user_id):
    params = {
        'user_id': user_id,
        'access_token': access_token,
        'extended': 0,
        'v': 5.101
    }
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        params=params
    )
    return response.json()


def onli_you_group(groups, friends):
    # Получаем множество групп всех друзей
    groups_friends = set()
    counter = 0
    friends_counter = 0
    print(f'У пользователя всего {friends["response"]["count"]} друзей ')
    for i in friends['response']['items']:
        friends_counter += 1
        print(f'Обрабатано {friends_counter} из {friends["response"]["count"]} друзей')
        time.sleep(0.2)
        group = get_group(i)
        # pprint(group)
        try:
            groups_friends.update(group['response']['items'])
        except KeyError:
            counter += 1
            continue
    print(f'\n\nПрограмме не получилось получить доступ к {counter} пользователям. \n'
          f'Так как их странички удалены или приватны')
    # Получаем множество групп в которых состоит только пользователь
    you_group = set(groups['response']['items']).difference(groups_friends)
    return you_group


def info_group(group_id):
    params = {
        'group_id': group_id,
        'access_token': access_token,
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
    groups = user.get_groups()
    print("Определили группы в которые входит пользователь")
    friends = user.get_friends()
    print("Нашли друзей пользователя ")
    you_group = onli_you_group(groups, friends)
    print("Нашли id групп в которые входит только наш пользователь ")
    file_load = []
    counter_end = len(you_group)
    counter = 0
    for group_id in you_group:
        counter += 1
        print(f'Получаем информацию о {counter} группе из {counter_end}')
        time.sleep(0.3)
        try:
            you_group = info_group(group_id)
            file_load.append(you_group)
        except KeyError:
            print(f'Не удалось получить информацию о группе {counter}')
            continue
    pprint(file_load)
    print("Вот группы в которых состоит только наш пользователь и никто из его друзей")
    print("Записываем json файл с описанием групп")
    write(file_load)
    print("Записали информацию в groups.json файл проверяйте")


execution()



# www = {1835300,
#  7669591,
#  8163141,
#  11305188,
#  23396502,
#  23907159,
#  26717401,
#  26896111,
#  28045060,
#  28423507,
#  28464680,
#  29156611,
#  30104734,
#  30358840,
#  30654771,
#  30812754,
#  30959591,
#  31048778,
#  31823187,
#  32359139,
#  32449555,
#  32515782,
#  32529823,
#  32916522,
#  33843101,
#  34166518,
#  34361759,
#  35466805,
#  35780861,
#  36667515,
#  36837512,
#  37676198,
#  37786906,
#  38278664,
#  39365644,
#  39645210,
#  40314048,
#  40913985,
#  40971498,
#  41032556,
#  41188472,
#  41208237,
#  41263105,
#  41520304,
#  41555605,
#  42286632,
#  43842216,
#  44853756,
#  45863690,
#  46596422,
#  47198437,
#  47756175,
#  47875773,
#  49730861,
#  49936536,
#  52187365,
#  53924330,
#  55391447,
#  55432580,
#  56277850,
#  57579363,
#  64213120,
#  70092551,
#  75343528,
#  88656999,
#  89204033,
#  104052522,
#  117893081,
#  134385259,
#  159873992}
#
#
# for i in www:
#     params = {
#         'group_id': i,
#         'access_token': access_token,
#         'fields': 'members_count',
#         'extended': 0,
#         'v': 5.101
#     }
#     response = requests.get(
#         'https://api.vk.com/method/groups.getById',
#         params=params
#     )
#     pprint(response.json())