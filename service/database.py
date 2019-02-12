from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from string import Template
import json

engine = create_engine('sqlite:///./test.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def update_junction_skills(junctions, user_skills):
	# what is a hashmap
	for junction in junctions:
		for skill in user_skills:
			if junction.skill_id == skill.id and junction.rating != skill.rating:
				junction.rating = skill.rating

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
		return session.query(Junction).filter_by(user_id=user.id, skill_id=skill.id), session

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
	
	@staticmethod
	def create(user, session=None):
		print(user)
		if session is None:
			session = Session()
			session.add(user)
			session.commit()
		else:
			session.add(user)

	def fetch():
		session = Session()
		for instance in session.query(User):
			print(instance)

	@staticmethod
	def get(id):
		session = Session()
		return session.query(User).filter_by(id=id).first(), session

	def toJson(self):
		return {
			"id": self.id,
			"name": self.name,
			"picture": self.picture,
			"company": self.company,
			"email": self.email,
			"phone": self.phone,
			"latitude": self.latitude,
			"longitude": self.longitude,
			"skills": list(map(lambda skill: skill.toJson(), self.skills))
		}

	def merge(self, obj, session = None):
		commit = False
		if session is None:
			session = Session()
			commit = True
		selfDict = self.toJson()
		for key in selfDict:
			attr = obj.get(key, None)
			if key == "id":
				continue
			elif attr is not None and type(attr) != list:
				setattr(self, key, attr)
			elif key == "skills":
				joinedList = selfDict.get(key) + attr
				updatedSkills = list(map(lambda skill: Skill.get_or_create(user=self, name=skill['name'], session=session), joinedList))
				junctions = list(map(lambda skill: Junction.get_by_user_skill(self, skill), updatedSkills))
				updatedJunctions = update_junction_skills(junctions, updatedSkills) 
				setattr(self, key, updatedSkills)
		if commit:
			session.commit()

class Skill(Base):
	__tablename__ = 'skills'
	id = Column(Integer, primary_key=True)
	name = Column(String(32))
	users = relationship("Junction", back_populates="skill")

	def  __repr__(self):
		return f'ID: {self.id}, NAME: {self.name}'

	def toJson(self):
		return {
			"id": self.id,
			"name": self.name,
		}

	@staticmethod
	def create(skill, session=None):
		if session is None:
			session = Session()
		session.add(skill)
		return skill, session

	@staticmethod
	def get(id):
		session = Session()
		return session.query(Skill).filter_by(id=id).first(), session

	@staticmethod
	def get_by_name(name, session=None):
		if session is None:
			session = Session()
		return session.query(Skill).filter_by(name=name).first(), session

	@staticmethod
	def get_or_create(user, name, session=None):
		junction, session = Skill.get_by_name(name, session)
		if junction is None:
			junction, session = Skill.create(Skill(name=name), session)

		return skill

def initialize_db():
	Base.metadata.create_all(engine)

def delete_db():
	Base.metadata.drop_all(engine)