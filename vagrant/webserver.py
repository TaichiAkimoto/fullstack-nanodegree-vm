from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def restaurant_List(self):
        restaurants = session.query(Restaurant).all()
        output = "<html><body>"
        output += "<a href='/restaurants/new'>Create a new restaurant</a>"
        for restaurant in restaurants:
            output += "<br/><br/><div> %s </div>" % restaurant.name
            output += "<a href='/restaurants/{0}/edit'>edit</a><br /><a href='/restaurants/{1}/delete'>delete</a>".format(restaurant.id, restaurant.id)
        output += "</body></html>"
        if output == "<html><body></body></html>":
            output = "No Restaurants Found"
        return output

    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id_number = self.path.split("/")[2]
                delete_restaurant = session.query(Restaurant).filter_by(id = id_number).all()
                if delete_restaurant != []:
                    output = "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{}/delete'><h1>Delete this restaurant {} from the list ?</h1><input type='submit' value='Delete'> </form>".format(id_number, delete_restaurant[0].name)
                    output += "</html></body>"
                    self.wfile.write(output)
                else:
                    self.wfile.write("Query Failed! Try again")
                return
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id_number = self.path.split("/")[2]
                output = "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><h1>Renamte this restaurant</h1><input name='message' type='text' ><input type='submit' value='Rename'> </form>" % id_number
                output += "</html></body>"
                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = self.restaurant_List()
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'><h1>Create a new restaurant</h1><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</html></body>"
                self.wfile.write(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                id_number = self.path.split("/")[2]
                deleteRestaurant = session.query(Restaurant).filter_by(id=id_number).one()
                session.delete(deleteRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers
                return
                
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                id_number = self.path.split("/")[2]
                renameRestaurant = session.query(Restaurant).filter_by(id=id_number).one()
                renameRestaurant.name = messagecontent[0]
                session.add(renameRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers
                return

            if self.path.endswith("/restaurants"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                myFirstRestaurant = Restaurant(name = messagecontent[0])
                session.add(myFirstRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            else:
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
