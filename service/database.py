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
	Column('skill_id',  Integer, ForeignKey('skills.id'))
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
	def create(user):
		session = Session()
		session.add(user)
		session.commit()

	def fetch():
		for instance in db_session.query(User):
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
			"skills": self.skills
		}

	@staticmethod
	def fromJson(jsonStr):
		user = json.loads(jsonStr)
		return User(name=user.name)

	def merge(self, obj):
		selfDict = self.toJson()
		for key in selfDict:
			attr = obj.get(key, None)
			if key == "id":
				continue
			elif attr is not None and type(attr) != list:
				setattr(self, key, attr)
			elif type(attr) == list:
				setattr(self, selfDict.get(key) + attr)

class Skill(Base):
	__tablename__ = 'skills'
	id = Column(Integer, primary_key=True)
	skillName = Column(String(32))
	rating = Column(Integer)
	def  __repr__(self):
		return f'ID: {self.id}, NAME: {self.skillName}, RATING: {self.rating}'

def initialize_db():
	Base.metadata.create_all(engine)
