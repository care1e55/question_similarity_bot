from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Questions(Base):
    __tablename__ = 'debug'
    __table_args__ = {'schema': 'telegrambot'}

    question = Column(String, primary_key=True)
    embedding = Column(String)

    def __repr__(self):
        return f'user_id={self.question}, email={self.embedding}'
