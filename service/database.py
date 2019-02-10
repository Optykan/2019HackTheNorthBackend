from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from string import Template
import json

engine = create_engine('sqlite:///./test.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

junction = Table('junction', Base.metadata, 
	Column('user_id', Integer, ForeignKey('users.id')),
	Column('skill_id',  Integer, ForeignKey('skills.id')),
	Column('rating', Integer)
)

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
	skills = relationship("Skill", secondary=junction, backref="users")
	
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
				updatedSkills = list(map(lambda skill: Skill.get_or_create(name=skill['name'], session=session), joinedList))
				setattr(self, key, updatedSkills)
		if commit:
			session.commit()

class Skill(Base):
	__tablename__ = 'skills'
	id = Column(Integer, primary_key=True)
	name = Column(String(32))
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
	def get_or_create(name, session=None):
		skill, session = Skill.get_by_name(name, session)
		if skill is None:
			skill, session = Skill.create(Skill(name=name), session)

		return skill

def initialize_db():
	Base.metadata.create_all(engine)

def delete_db():
	Base.metadata.drop_all(engine)