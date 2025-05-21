from sqlalchemy import Column, String, MetaData, Integer, ForeignKey, BigInteger, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

metadata_obj = MetaData()


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata_obj


class ServerConf(Base):
    __tablename__ = "server_conf"

    private_key = Column(String, primary_key=True, nullable=False)
    allowed_ips = Column(String, nullable=False, unique=True)
    listen_port = Column(Integer, nullable=False, unique=True)
    pre_up = Column(String)
    post_up = Column(String)
    pre_down = Column(String)
    post_down = Column(String)


class WgConfList(Base):
    __tablename__ = "conf_list"

    conf_id = Column(String, primary_key=True)
    public_key = Column(String, nullable=False, unique=True)
    private_key = Column(String, nullable=False, unique=True)
    preshared_key = Column(String, nullable=False, unique=True)
    allowed_ips = Column(String, nullable=False, unique=True)
    valid_until = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)


class UserList(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger,primary_key=True)
    username = Column(String,nullable=False)
    register_date = Column(String,nullable=False)
    used_demo = Column(Boolean,nullable=False)


class UserConfList(Base):
    __tablename__ = "user_conf_list"

    user_id = Column(BigInteger,ForeignKey("users.user_id",ondelete="CASCADE"),primary_key=True)
    conf_id = Column(String,ForeignKey("conf_list.conf_id",ondelete="CASCADE"),primary_key=True)


