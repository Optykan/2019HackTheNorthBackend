from sqlalchemy import Column, Integer, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import AssertType, assert_type
import numbers

engine = create_engine('sqlite:///./test.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# The Junction table is an association object between Users and Skills
# It's a variation of many to many but with extra fields
class Junction(Base):
    __tablename__ = 'junction'
    junction_id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    skill_id = Column('skill_id', Integer, ForeignKey('skills.id'))
    user_skill_rating = Column('rating', Integer)
    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="users")

    @staticmethod
    def get_by_user_skill(user, skill, session=None):
        if session is None:
            session = Session()

        return session.query(Junction).filter_by(user_id=user.id, skill_id=skill.id)

    # link a skill to a user through the junction
    def link(self, skill, user):
        user.skills.append(self)
        self.skill = skill

    # return the dictionary representation of this junction
    def represent_as_skill(self):
        return {
            "name": self.skill.name,
            "rating": self.user_skill_rating,
        }

    @staticmethod
    def retrieve(user, skill, session=None):
        if session is None:
            session = Session()
        return session.query(Junction).filter_by(user_id=user.id, skill_id=skill.id)

    @staticmethod
    def retrieve_all():
        session = Session()
        ret = []
        for junction in session.query(Junction):
            ret.append(junction)
        return ret

# A User object
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    picture = Column(String(100))
    company = Column(String(50))
    email = Column(String(50))
    phone = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    skills = relationship("Junction", back_populates="user")

    def __repr__(self):
        return f'ID: {self.id}, NAME: {self.name}'

    def update_user(self, obj, session):
        # serialize self to json so we can iterate over properties
        # I'm sure theres a better way but I'm a JS programmer
        selfDict = self.to_json()
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
                # existing_junctions = session.query(Junction).filter_by(user_id=self.id)
                # junction_objs = []
                # for junction in existing_junctions:
                #  junction_objs.append(junction)

                # 2) Find missing Junctions and create them
                # 3) update the junctions
                # 4) save junctions

                # As it currently stands we assume we're just creating a user
                skill_objects = list(map(lambda dict: Skill(name=dict['name'], rating=dict['rating']), attr))
                db_safe = list(map(lambda skill: Skill.get_or_create(self, skill, session)[1], skill_objects))
                setattr(self, "skills", db_safe)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture": self.picture,
            "company": self.company,
            "email": self.email,
            "phone": self.phone,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "skills": list(map(lambda junction: junction.represent_as_skill(), self.skills))
        }

    @staticmethod
    def retrieve_all():
        session = Session()
        users = []
        for user in session.query(User):
            users.append(user.to_json())
        session.close()
        return users

    @staticmethod
    def create(user, session=None):
        if session is None:
            session = Session()
            session.add(user)
            session.commit()
            session.close()
        else:
            session.add(user)

    @staticmethod
    def get_by_id(user_id, session=None):
        if session is None:
            session = Session()
        return session.query(User).filter_by(id=user_id).first(), session

    # Validate the current values on this object
    def validate(self):
        types = {
            "id": AssertType(int),
            "name": AssertType(str, 50),
            "picture": AssertType(str, 100),
            "company": AssertType(str, 50),
            "email": AssertType(str, 50),
            "phone": AssertType(str, 20),
            "latitude": AssertType(type=numbers.Number, check_range=True, minimum=-90, maximum=90),
            "longitude": AssertType(type=numbers.Number, check_range=True, minimum=-180, maximum=180),
        }
        assert_type(self.to_json(), types)


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    users = relationship("Junction", back_populates="skill")
    rating = 0

    def __repr__(self):
        return f'Name: {self.name}'

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def get_by_name(skillName, session=None):
        if session is None:
            session = Session()
        return session.query(Skill).filter_by(name=skillName).first(), session

    @staticmethod
    def create(skill, session=None):
        if session is None:
            session = Session()
            session.add(skill)
            session.commit()
            session.close()
        else:
            session.add(skill)

    @staticmethod
    def get_or_create(user, input_skill, session=None):
        skill, session = Skill.get_by_name(input_skill.name, session)
        if skill is None:
            skill = Skill(name=input_skill.name)
            Skill.create(skill, session)
        junction = Junction(user_skill_rating=input_skill.rating)
        junction.link(user=user, skill=skill)
        return skill, junction, session

    @staticmethod
    def create_if_not_exists(skill, session=None):
        retr_skill, session = Skill.get_by_name(skill['name'], session)
        if skill is None:
            skill = Skill(name=input_skill['name'])
            Skill.create(skill, session)

    @staticmethod
    def retrieve_all():
        session = Session()
        results = session.query(Skill)
        ret = []
        for skill in results:
            ret.append(skill.to_json())
        session.close()
        return ret


# Create the tables
def initialize_db():
    Base.metadata.create_all(engine)


# Delete the tables
def delete_db():
    Base.metadata.drop_all(engine)
