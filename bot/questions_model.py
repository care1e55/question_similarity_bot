from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Questions(Base):
    __tablename__ = 'debug'
    __table_args__ = {'schema': 'telegrambot'}

    question = Column(String, primary_key=True)
    message_id = Column(String) 
    embedding = Column(String)

    def __repr__(self):
        return f'''
            question={self.question}, 
            message_id={self.message_id},
            embedding={self.embedding}
            '''
