from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def main():
    myFirstRestaurant = Restaurant(name = "Pizza Palace")
    session.add(myFirstRestaurant)
    session.commit()

if __name__ == '__main__':
    main()
