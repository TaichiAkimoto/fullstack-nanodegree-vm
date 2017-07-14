from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def main():

    # This is where the bulk operations will be done.
    # s = Session()
    # objects = [
    # User(name="u1"),
    # User(name="u2"),
    # User(name="u3")
    # ]
    # s.bulk_save_objects(objects)
    #objects1 = [
    #    Restaurant(name='The CRUDdy Crab'),
    #    Restaurant(name='Blue Burgers'),
    #    Restaurant(name='Taco Hut'),
    #]
    #object2 = [
        #MenuItem(name='Cheese Pizza',description='made with fresh cheese',price='$5.99',course='Entree'),
        #MenuItem(name='Chocolate Cake',description='made with Dutch Chocolate',price='$3.99',course='Dessert'),
        #MenuItem(name='Caesar Salad',description='with fresh organic vegetables',price='$5.99',course='Entree'),
    #]
    firstMenu = session.query(MenuItem).all()
    for item in firstMenu:
        print item.name
        print item.course
        print item.description
        print item.id

if __name__ == '__main__':
    main()
