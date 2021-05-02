import datetime
import os
import time
from hashlib import pbkdf2_hmac, blake2b
from hmac import compare_digest

from flask import g
from sqlalchemy import (
    Column, Integer, DateTime, Table,
    TIMESTAMP, Boolean, String, ForeignKey, Text)
from sqlalchemy.orm import relationship, declared_attr
from . import db


class TimestampMixin(object):
    dt_format_aware = time.strftime(
        "%d.%m.%Y %H:%M:%S UTC%z", time.localtime())
    created = Column(
        DateTime, nullable=False, default=datetime.datetime.now)
    updated = Column(
        DateTime, onupdate=datetime.datetime.now)


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String, default=os.urandom(5).hex('X', 3),
                       nullable=False)
    login = Column(String(20), nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(50), nullable=True)
    name = Column(String(50), default='Chef')

    def __init__(self, login, password):
        self.password = self.set_pwd_hash(login, password)
        self.login = login
        self.public_id = os.urandom(5).hex('Y', 3)

    def set_pwd_hash(self, login, password):
        persona = login.encode('utf-8')  # must be bytes
        pwd = password.encode('utf-8')  # pwd must be bytes
        sec_key = str(os.getenv('SECRET_KEY', os.urandom(16).hex('A', 13))
                      ).encode('utf-8')
        salted = os.urandom(blake2b.SALT_SIZE)
        hashed = blake2b(salt=salted, digest_size=32, key=sec_key,
                         person=persona)
        hashed.update(pwd)
        pwd_hashed = hashed.hexdigest()
        return pwd_hashed

    def public_data(self):
        """Serialize record output without password"""
        return {
            "user_id": self.public_id,
            "name": self.name,
            }

    @staticmethod
    def login_validation(pwd, current_pass=password, pub=public_id):
        if compare_digest(current_pass, pwd):
            return pub
        else:
            return False


# for mm relation
assoc_menu_dish = Table(
    "menu_dishes", db.Model.metadata,
    Column("menu_id", Integer, ForeignKey("menu_card.id"), nullable=True),
    Column("dish_id", Integer, ForeignKey("dish.id"), nullable=True))


class MenuCard(db.Model):
    __tablename__ = 'menu_card'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(200), nullable=False, default='deliciousness?')
    vegetarian_card = Column(Boolean)
    public_card = Column(Boolean)

    # dishes

    def __repr__(self):
        return self.name

    # for m-m relation
    dishes = relationship(
        "Dish", secondary=assoc_menu_dish, backref="menu_card")

    created_on = Column(DateTime,
                        default=time.strftime(
                            "%d.%m.%Y %H:%M:%S UTC%z",
                            time.localtime()), nullable=False)
    changed_on = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now, nullable=False)

    @declared_attr
    def created_by_fk(cls):
        return Column(Integer, ForeignKey("ab_user.id"),
                      default=cls.get_user_id, nullable=False
                      )

    @declared_attr
    def created_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.created_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
            )

    @declared_attr
    def changed_by_fk(cls):
        return Column(
            Integer,
            ForeignKey("ab_user.id"),
            default=cls.get_user_id,
            onupdate=cls.get_user_id,
            nullable=False,
            )

    @declared_attr
    def changed_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.changed_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
            )

    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return None


class Dish(db.Model):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(200), nullable=False, default='delicious?')
    price = Column(String(6), nullable=False, default='9.99')
    preparation_time = Column(Integer, nullable=False, default=30)
    vegetarian = Column(Boolean)
    menu_card = relationship(
        "MenuCard", secondary=assoc_menu_dish, backref='dishes')
    # menu_id = Column(Integer, ForeignKey('menu_card.id'))
    image_thumbnail = Column(Text)

    def __repr__(self):
        return self.name

    # def get_timestamp():
    #     return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    created_on = Column(DateTime,
                        default=time.strftime(
                            "%d.%m.%Y %H:%M:%S UTC%z",
                            time.localtime()), nullable=False)
    changed_on = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now, nullable=False)

    @declared_attr
    def created_by_fk(cls):
        return Column(Integer, ForeignKey("ab_user.id"),
                      default=cls.get_user_id, nullable=False
                      )

    @declared_attr
    def created_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.created_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
            )

    @declared_attr
    def changed_by_fk(cls):
        return Column(
            Integer,
            ForeignKey("ab_user.id"),
            default=cls.get_user_id,
            onupdate=cls.get_user_id,
            nullable=False,
            )

    @declared_attr
    def changed_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.changed_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
            )

    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return None
