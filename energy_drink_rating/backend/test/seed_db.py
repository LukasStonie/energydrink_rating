# Import the classes and Base from your original file
from backend.dataLayer.DatabaseConnector import DatabaseConnector
from backend.dataLayer.Models import Comb, Drink, DrinkType, Review, User
from sqlalchemy.orm import sessionmaker


def seed_database():

    # 1. Setup the connection
    engine = DatabaseConnector().engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # 2. Create Drink Types
    soda = DrinkType(name="Soda")
    juice = DrinkType(name="Juice")
    session.add_all([soda, juice])
    session.commit()  # Commit to get IDs for the types

    # 3. Create individual Drinks
    cola = Drink(brand="Coca-Cola", flavor="Classic", drink_type=soda)
    cherry = Drink(brand="Generic", flavor="Cherry Syrup", drink_type=soda)
    orange = Drink(brand="Tropicana", flavor="Orange", drink_type=juice)
    session.add_all([cola, cherry, orange])

    # 4. Create a User
    bob = User(username="BobTheMixer", password_hash="hasdfasdf")
    session.add(bob)
    session.commit()

    # 5. Create a Combination (The Mix)
    # Note: We add the drink objects directly to the .drinks list
    cherry_cola = Comb(name="Cherry Cola Special")
    cherry_cola.drinks.append(cola)
    cherry_cola.drinks.append(cherry)

    session.add(cherry_cola)
    session.commit()

    # 6. Add a Review for that Combination
    review = Review(
        rating=5,
        comment="Perfect balance of cherry and fizz!",
        user=bob,
        combination=cherry_cola
    )

    session.add(review)
    session.commit()

    print("Seed data added successfully!")


if __name__ == "__main__":
    seed_database()
