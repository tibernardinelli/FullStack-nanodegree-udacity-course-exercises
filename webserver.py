from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/restaurants":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            restaurants = session.query(Restaurant).all()
            template_restaurant_item = open("pages/restaurant_item.html", "r").readline()
            for line in open("pages/restaurants.html", "r").readlines():
                _line = line[:-1]
                if (_line == "<replace_tag/>"):
                    print(restaurants)
                    for restaurant in restaurants:
                        #self.wfile.write("<li>" + restaurant.name + "</li>")
                        self.wfile.write(template_restaurant_item % (restaurant.name,restaurant.id, restaurant.id))
                        print(restaurant.name)
                else:
                    self.wfile.write(_line)            
            return
        elif self.path == "/restaurants/new":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = open("pages/new_restaurants.html", "r")
            for line in message.readlines():                
                self.wfile.write(line)
                print(line)
            message.close()
            return
        
        else:
            try:
                print(self.path[1:] + ".html")
                message = open("pages/" + self.path[1:] + ".html", "r")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                for line in message.readlines():                
                    self.wfile.write(line)
                    print(line)
                message.close()
                return
            except:
                self.send_error(404, 'File Not Found: %s' % self.path)

     
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            message = ""
            message += "<html><body>"
            message += " <h2> Okay, how about this: </h2>"
            message += "<h1> %s </h1>" % messagecontent[0]
            message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            message += "</body></html>"
            self.wfile.write(message)
            print(message)
        except:
            pass                 

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()