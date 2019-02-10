import json
from service.database import User, Skill, Session

def create_users(data):
	session = Session()
	for d in data:
		print(d['name'])
		user = User(name='hi')
		user.merge(d, session)
		User.create(user, session)
	session.commit()
	print('Created Users')

def create_skills(all_data):
	session = Session()
	for user in all_data:
		skills = user['skills']
		for skill in skills:
			#hello, O(n^2)
			Skill.create(Skill(name=skill['name']), session)
	session.commit()
	print('Created skills')

def load_database():
	json_file = open('./scripts/users.json').read()
	raw_data = json.loads(json_file)
	create_skills(raw_data)
	create_users(raw_data)
	
	print('Loaded database')
