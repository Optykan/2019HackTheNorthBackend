from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from string import Template

engine = create_engine('sqlite:///test.db:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db_session = Session()

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
	
	def create(user):
		db_session.add(user)
		db_session.commit()

	def fetch():
		for instance in db_session.query(User):
			print(instance)


class Skill(Base):
	__tablename__ = 'skills'
	id = Column(Integer, primary_key=True)
	skillName = Column(String(32))
	rating = Column(Integer)
	def  __repr__(self):
		return f'ID: {self.id}, NAME: {self.skillName}, RATING: {self.rating}'

def initialize_db():
	Base.metadata.create_all(engine)
