import vk_api
import json
import datetime

class VkApi:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()

    def get_user_data_by_id(self, user_ids):
        users_data = self.vk.users.get(user_ids=user_ids, fields='about,activities,bdate,blacklisted,blacklisted_by_me,books,can_post,can_see_all_posts,can_see_audio,can_send_friend_request,can_write_private_message,career,city,common_count,connections,contacts,counters,country,crop_photo,deactivated,education,exports,first_name,followers_count,friends_count,games,has_mobile,has_photo,home_town,interests,is_favorite,is_friend,is_hidden_from_feed,last_name,lists,maiden_name,military,movies,music,nickname,occupation,online,personal,photo_100,photo_200,photo_50,photo_id,quotes,relatives,relation,schools,screen_name,sex,site,status,status_audio,timezone,trending,universities,verified,wall_comments,was_online')
        return users_data

    def save_user_data_to_file(self, user_data):
        user_id = user_data['id']
        folder_path = f'users/{user_id}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        filename = f'{folder_path}/{user_id}_{datetime.utcnow().strftime("%d.%m.%Y-%H:%M:%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def compare_json_objects(old_version, new_version):
        if isinstance(old_version, str):
            old_version = json.loads(old_version)
        if isinstance(new_version, str):
            new_version = json.loads(new_version)

        fields_changed = []
        old_fields = []
        new_fields = []

        for key in old_version:
            if key not in new_version:
                old_fields.append(key)
            elif old_version[key] != new_version[key]:
                fields_changed.append((key, new_version[key]))

        for key in new_version:
            if key not in old_version:
                new_fields.append((key, new_version[key]))

        return fields_changed, old_fields, new_fields

    def load_user_data_from_file(self, user_id):
        user_dir = os.path.join('users', str(user_id))
        if not os.path.exists(user_dir) or not os.listdir(user_dir):
            return None
        
        json_files = [f for f in os.listdir(path) if f.endswith('.json')]
        if not json_files:
            return None
        
        latest_file = max(json_files, key=lambda f: datetime.strptime(f.split('_')[-1], "%d.%m.%Y-%H:%M:%S"))
        with open(os.path.join(path, latest_file), 'r') as f:
            data = json.load(f)
        return data

    def work(self, users_data):
        for user_data in users_data:
            user_id = user_data['id']
            old_data = self.load_user_data_from_file(user_id)
            if old_data is not None:
                fields_changed, old_fields, new_fields = self.compare_json_objects(old_data, user_data)
                if not fields_changed and not old_fields and not new_fields:
                    continue
            self.save_user_data_to_file(user_data)