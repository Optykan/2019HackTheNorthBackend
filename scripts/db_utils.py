import json
from models import User, Skill, Session

def create_from_dict(obj, session):
	user = User()
	user.update_user(obj, session)
	return user


def create_users(data):
	session = Session()
	for d in data:
		user = create_from_dict(d, session)
		User.create(user, session)
	session.commit()
	print('Created Users')


def create_skills(all_data):
	session = Session()
	for user in all_data:
		skills = user['skills']
		for skill in skills:
			Skill.create_if_not_exists(skill, session)

	session.commit()
	print('Created skills')


def load_database():
	json_file = open('./scripts/users.json').read()
	raw_data = json.loads(json_file)
	print("Create skills")
	create_skills(raw_data)
	print("Create users")
	create_users(raw_data)
	
	print('Loaded database')
