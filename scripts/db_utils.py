import json
from models import User, Skill, Session

# create a user from a dictionary object
def create_from_dict(obj, session):
    user = User()
    user.update_user(obj, session)
    return user


# create all the users and save them
def create_users(data):
    session = Session()
    for d in data:
        user = create_from_dict(d, session)
        User.create(user, session)
    session.commit()
    print('Created Users')


# create all the skills, once only
def create_skills(all_data):
    session = Session()
    for user in all_data:
        skills = user['skills']
        for skill in skills:
            Skill.create_if_not_exists(skill, session)

    session.commit()
    print('Created skills')


# read the data into the database
def load_database():
    json_file = open('./scripts/users.json').read()
    raw_data = json.loads(json_file)
    print("Create skills")
    create_skills(raw_data)
    print("Create users")
    create_users(raw_data)

    print('Loaded database')
