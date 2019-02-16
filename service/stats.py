from models import User, Skill, Junction, Session
from sqlalchemy import func
from functools import reduce


# query all the users with this skill and take the average
def average_skill_rating(skill_id):
	session = Session()
	junctions = session.query(Junction).filter_by(skill_id=skill_id)

	# I'm sure there's a sql way to take an average
	rating = []
	for junction in junctions:
		rating.append(junction.user_skill_rating)

	if len(rating) == 0:
		return 0

	session.close()
	# not sure how python treats floating point values
	return sum(rating)/len(rating)


# return the count of users with a certain skill id
def users_with_skill(skill_id):
	session = Session()
	ret = session.query(Junction).filter_by(skill_id=skill_id).count()
	session.close()
	return ret


# to be plugged into filter(), returns a skill if it matches the params
def filter_stats(skill, min_rating=0, max_rating=10, min_frequency=0, max_frequency=-1):
	if max_frequency == -1:
		return skill['average'] >= min_rating and skill['average'] <= max_rating and skill['count'] >= min_frequency
	return skill['average'] >= min_rating and skill['average'] <= max_rating and skill['count'] >= min_frequency and skill['count'] <= max_frequency
