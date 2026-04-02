from backend.dataLayer.DatabaseConnector import DatabaseConnector
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# 1. Association Table for Drinks <-> Comb (Many-to-Many)
# Uses a composite primary key as requested.


class Drinks2Comb(Base):
    __tablename__ = 'drinks2comb'
    drink_id = Column(Integer, ForeignKey('drinks.id'), primary_key=True)
    comb_id = Column(Integer, ForeignKey('comb.id'), primary_key=True)

# 2. DrinkType Table


class DrinkType(Base):
    __tablename__ = 'drink_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    drinks = relationship("Drink", back_populates="drink_type")

# 3. Drinks Table


class Drink(Base):
    __tablename__ = 'drinks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String)
    name = Column(String)
    type_id = Column(Integer, ForeignKey('drink_types.id'))

    drink_type = relationship("DrinkType", back_populates="drinks")

    # Many-to-many relationship to Comb via Drinks2Comb
    combinations = relationship(
        "Comb", secondary="drinks2comb", back_populates="drinks")

# 4. Users Table


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String)
    password_hash = Column(String, nullable=False)
    reviews = relationship("Review", back_populates="user")

# 5. Reviews Table


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Integer)
    comment = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    comb_id = Column(Integer, ForeignKey('comb.id'))

    user = relationship("User", back_populates="reviews")
    combination = relationship("Comb", back_populates="reviews")

# 6. Comb Table (Combinations)


class Comb(Base):
    __tablename__ = 'comb'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    # Many-to-many relationship to Drink via Drinks2Comb
    drinks = relationship("Drink", secondary="drinks2comb",
                          back_populates="combinations")

    reviews = relationship("Review", back_populates="combination")


if __name__ == "__main__":
    conn = DatabaseConnector()
    Base.metadata.create_all(conn.engine)
