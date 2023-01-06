from database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class UserPost(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    is_published = Column(Boolean, server_default = "TRUE", nullable = False)
    created = Column(TIMESTAMP(timezone=True), server_default = text("now()"), nullable = False)
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    created = Column(TIMESTAMP(timezone=True), server_default = text("now()"), nullable = False)


class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


    
