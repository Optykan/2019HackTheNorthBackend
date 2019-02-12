from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from string import Template
from collections import namedtuple
import json

engine = create_engine('sqlite:///./test.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Junction(Base):
	__tablename__ = 'junction'
	junction_id = Column(Integer, primary_key=True)
	user_id = Column('user_id', Integer, ForeignKey('users.id'))
	skill_id = Column('skill_id',  Integer, ForeignKey('skills.id'))
	user_skill_rating = Column('rating', Integer)
	user = relationship("User", back_populates="skills")
	skill = relationship("Skill", back_populates="users")	

	@staticmethod
	def get_by_user_skill(user, skill, session=None):
		if session is None:
			session = Session()
		return session.query(Junction).filter_by(user_id=user.id, skill_id=skill.id)

	@staticmethod
	def link(junction, skill, user)
		user.skills.append(junction)
		junction.skill = skill

	@staticmethod
	def retrieve(user, skill, session=None):
		if session is None:
			 
		return

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	picture = Column(String(100))
	company = Column(String(50))
	email = Column(String(50))
	phone = Column(String(10))
	latitude = Column(Float)
	longitude = Column(Float)
	skills = relationship("Junction", back_populates="user")
	
	def  __repr__(self):
		return f'ID: {self.id}, NAME: {self.name}, ...'

	def update(self, obj, session):
		#serialize self to json so we can iterate over properties
		#I'm sure theres a better way but I'm a JS programmer
		selfDict = self.toJson()
		for key in selfDict:
			attr = obj.get(key, None)
			if key == "id":
				# don't update the id
				continue
			elif attr is not None and type(attr) != list:
				# regular attributes
				setattr(self, key, attr)
			elif key == "skills":
				# to update the skills, we need to:
				# 1) fetch all the Junctions
				# 2) Find missing Junctions and create them
				# 3) update the junctions
				# 4) save junctions 
				setattr(self, key, updatedSkills)

class Skill(Base):
	__tablename__ = 'skills'
	id = Column(Integer, primary_key=True)
	name = Column(String(50))

	@staticmethod
	def get_by_name(skillName, session=None):
		if session is None:
			session = Session()
		return session.query(Skill).filter_by(name=skillName).first(), session

	@staticmethod
	def create(skill, session=None):
		if session is None
			session = Session()
			session.add(skill)
			session.commit()
		else
			session.add(skill)

	@staticmethod
	def fromJson(json):





