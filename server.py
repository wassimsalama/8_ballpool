import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import Physics as Physics;
import os;
import json;
from urllib.parse import parse_qs

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qs;
database = Physics.Database()
database.createDB()
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse (self.path);
            
            if parsed.path == "/index.html":
                self.serve_file('index.html')
            elif parsed.path == "/table.html":
                self.serve_file('table.html')

            elif parsed.path.startswith ("/initial"):
                
                print(f"Original query string: {parsed}") 
                table_id = parse_qs(parsed.query).get('table_id',['0'])[0]
                
                table = database.readTable(int(table_id))
         

                
                if table is not None:
                    table_content =  table.svg()
                else:
                    table_content =  None
             
                dump = json.dumps({"svg":table_content})
                self.send_response(200)
                self.send_header('Content-Type','application/json')
                self.end_headers()
                self.wfile.write(dump.encode('utf-8'))
    
        def serve_file(self, file_path):
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File not found.")

        def do_POST(self):
            print(f"Received POST request on {self.path}") 
            parsed = urlparse(self.path)

            if parsed.path.startswith ('/process-shot'):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(post_data)  # Assuming JSON data
        
        # Extract deltaX and deltaY from the posted data
                deltaX = data.get('deltaX')
                deltaY = data.get('deltaY')
                game_id = data.get('game_id')
                table_id = data.get('table_id')
        # Here you would calculate the initial velocity and update the simulation
        # For example, just printing the values
                

                game = Physics.Game(game_id)

                table = game.db.readTable(table_id)
                
                table_array = game.shoot(game.gameName,game.player1Name,table,deltaX,deltaY)
                
                table_id = game.tableID
        
        # Respond to the client to confirm receipt of the data
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'status': 'success', 'message': 'Shot data processed.', 'array':table_array,'tableID':game.tableID})
                self.wfile.write(response.encode('utf-8'))

            if parsed.path == '/start':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = parse_qs(post_data)
                player1_name = data.get('player1')[0]
                player2_name = data.get('player2')[0]
 
                if player1_name and player2_name:
             
                    game = Physics.Game(None,"8 ball Pool" , player1_name , player2_name)
                    
                    
                    game_id = game.gameID
                    table_id = game.tableID
                    
                    self.send_response(303)
                    self.send_header("Location",f'/table.html?game_id={game_id}&table_id={table_id}&player1={player1_name}&player2={player2_name}')
                    self.end_headers()
                else:
               
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'status': 'error', 'message': 'Player names are required.'})
                    self.wfile.write(response.encode('utf-8'))
            
if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), SimpleHTTPRequestHandler  );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();