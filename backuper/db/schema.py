from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import INET, JSONB, CIDR
from sqlalchemy.orm import relationship
from backuper.db.base import Base


class Method(Base):
    __tablename__ = 'methods'
    id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', String, nullable=False, unique=True)
    description = Column('description', String)
    actions = Column('actions', JSONB)


class Subnet(Base):
    __tablename__ = 'subnets'
    id = Column('id', Integer, primary_key=True, nullable=False)
    subnet = Column('subnet', CIDR)
    folder = Column('folder', String, server_default='')
    enabled = Column('enabled', Boolean, server_default='true')


class DistinctDevice(Base):
    __tablename__ = 'distinct_devices'
    id = Column('id', Integer, primary_key=True, nullable=False)
    enabled = Column('enabled', Boolean, server_default='true')
    ip_address = Column('ip_address', INET)
    folder = Column('folder', String, server_default='')
    device_name = Column('device_name', String)
    method_name = Column(ForeignKey('methods.name'))
    method = relationship(Method)


class Model(Base):
    __tablename__ = 'models'
    id = Column('id', Integer, primary_key=True, nullable=False)
    model = Column('model', String)
    method_name = Column(ForeignKey(Method.name))
    method = relationship(Method)
