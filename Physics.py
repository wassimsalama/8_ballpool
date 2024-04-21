import phylib;
import Physics as Physics;
import sqlite3
import os
import math

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS  = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH  = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE  = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON  = phylib.PHYLIB_VEL_EPSILON;
DRAG  = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_RATE = 0.01;
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";
# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];  

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
                                       
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;
        


    # add an svg method here
    def svg(self):
        color = BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)]
        if(self.obj.still_ball.number == 0 ):
            return """<circle id="cueball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, color)
        return """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, color)
################################################################################

class Table( phylib.phylib_table ):

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
            # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                Coordinate(0,0),
                Coordinate(0,0),
                Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
# create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
# add ball to table
                new += new_ball;
# return table
        return new;
    """
    Pool table class.
    """
    def cueBall(self):
        for obj in self:
            if isinstance(obj, (StillBall, RollingBall)) and (obj.obj.still_ball.number == 0 or obj.obj.rolling_ball.number==0):
                return obj
        return None


    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
       
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        svg_content = HEADER
        for obj in self:
            if obj is not None:  # Check if the object is not None
                svg_content += obj.svg()
        svg_content += FOOTER
        return svg_content
    
   

class RollingBall( phylib.phylib_object ):
    def __init__(self, number , pos , vel , acc):
         # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel , acc , 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingClass
        self.__class__ = RollingBall;
    def svg(self):
        color = BALL_COLOURS[self.obj.rolling_ball.number % len(BALL_COLOURS)]
        if(self.obj.rolling_ball.number == 0 ):
            return """ <circle id = "cueball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, color)   
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, color)


class Hole(phylib.phylib_object):
    def __init__(self,pos):
        phylib.phylib_object.__init__(self,phylib.PHYLIB_HOLE,0,pos,None,None,0.0,0.0);
    # this converts the phylib_object into a Hole
        self.__class__= Hole;
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y , HOLE_RADIUS)


class HCushion(phylib.phylib_object):
    def __init__(self, y):
        phylib.phylib_object.__init__(self,phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y)

    def svg(self):
        y_position = -25 if self.obj.hcushion.y < Physics.TABLE_LENGTH / 2 else 2700
        return  """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y_position,)

class VCushion(phylib.phylib_object):
    def __init__(self,x):
        phylib.phylib_object.__init__(self,phylib.PHYLIB_VCUSHION,0,None,None,None,x,0.0)
        # this converts the phylib_object into a VCushion
        self.__class__ = VCushion;
    def svg(self):
        x_position = -25 if self.obj.vcushion.x < Physics.TABLE_WIDTH / 2 else 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x_position,)



class Database:
    def __init__(self, reset=False):
        self.db_path = 'phylib.db'  # Database file name
        if reset :
            os.remove(self.db_path) 
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.createDB()

    
    def recordTableShot(self, tableID, shotID,commit=True):
            self.cursor.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableID, shotID))
            if commit:
                self.conn.commit()

    def createDB(self):
        commands = [ """CREATE TABLE IF NOT EXISTS Ball (
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT
        );""", """CREATE TABLE IF NOT EXISTS  TTable(
    TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    TIME FLOAT NOT NULL
);""", """CREATE TABLE IF NOT EXISTS BallTable(
    BALLID INTEGER NOT NULL,
    TABLEID INTEGER NOT NULL,
    FOREIGN KEY(BALLID) REFERENCES Ball(BALLID),
    FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID)
);""","""CREATE TABLE IF NOT EXISTS Shot(
    SHOTID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL, 
    PLAYERID INTEGER NOT NULL,
    GAMEID INTEGER NOT NULL,
    FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
    FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
);""", """ CREATE TABLE IF NOT EXISTS TableShot(
    TABLEID INTEGER NOT NULL,
    SHOTID INTEGER NOT NULL,
    PRIMARY KEY (TABLEID, SHOTID),
    FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
    FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
    );""" ,"""CREATE TABLE IF NOT EXISTS Game(
    GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    GAMENAME VARCHAR(64) NOT NULL
    );""" , """ CREATE TABLE IF NOT EXISTS  Player (
    PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    GAMEID INTEGER NOT NULL,
    PLAYERNAME VARCHAR(64) NOT NULL,
    FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
    );""" 
        ]
        for command in commands:
            self.cursor.execute(command)
    
        self.conn.commit()

    def readTable(self , TableID):
        new_TableID  = TableID 
        table = Table()
        self.cursor.execute("SELECT TIME FROM TTABLE WHERE TABLEID=?", (new_TableID,))
        table_time_result = self.cursor.fetchone()
        if not table_time_result:
            return None  # TABLEID does not exist

        table_time = table_time_result[0]
        table.time = table_time

        self.cursor.execute("""
        SELECT  b.BALLNO, b.XPOS, b.YPOS, b.XVEL, b.YVEL
        FROM Ball b
        INNER JOIN BallTable  ON b.BALLID = BallTable.BALLID
        WHERE BallTable.TABLEID=?
    """, (new_TableID,))
        for ball_no, xpos, ypos, xvel, yvel in self.cursor.fetchall():
            pos = Coordinate(xpos, ypos)
            if xvel is None and yvel is None:
                new_ball = StillBall(ball_no, pos)
            else:    
                vel_rb = Coordinate(xvel,yvel)
                speed_rb = vel_rb.x * vel_rb.x + vel_rb.y * vel_rb.y
                acc_rb = Coordinate(0.0, 0.0)
                if speed_rb > VEL_EPSILON:
                    acc_rb.x = xvel / speed_rb * DRAG
                    acc_rb.y = yvel / speed_rb * DRAG
                    new_ball = RollingBall(ball_no,pos,vel_rb,acc_rb)
            table += new_ball
            
        return table

    def writeTable(self, table , commit= True):
    # Insert the table time into the TTable and get the autoincremented TABLEID
        self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = self.cursor.lastrowid     # Adjust for zero-based indexing preferred in your application

    # Iterate over objects in the table
        for obj in table:
        # Check if the object is a ball and should be stored
            if isinstance(obj, (StillBall, RollingBall)):
                xvel, yvel = (obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y) if isinstance(obj, RollingBall) else (None, None)
             # Insert the ball into the Ball table
                self.cursor.execute("""
                 INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                 VALUES (?, ?, ?, ?, ?)
           """, ( obj.obj.still_ball.number , obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y, xvel, yvel))   
                ball_id = self.cursor.lastrowid

            # Link the ball to the table in the BallTable
                self.cursor.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id ))
        if commit:
            self.conn.commit()

        return table_id  #-1
    def close(self):
        self.conn.commit()
        self.conn.close()
        
    def getGame(self, gameID):
        self.cursor.execute("""
            SELECT Game.GAMENAME, Player.PLAYERNAME
            FROM Game
            JOIN Player ON Game.GAMEID = Player.GAMEID
            WHERE Game.GAMEID = ?
            ORDER BY Player.PLAYERID ASC
        """, (gameID,))
        results = self.cursor.fetchall()
        if not results:
            return None
        gameName = results[0][0]
        player1Name = results[0][1]
        player2Name = results[1][1] if len(results) > 1 else None
        return gameName, player1Name, player2Name

    def setGame(self, gameName, player1Name, player2Name):
        self.cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        game_id = self.cursor.lastrowid
        self.cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player1Name))
        self.cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player2Name))
        self.conn.commit()
        return game_id
    def newShot(self, gameID, playerName):
        # Retrieve playerID based on playerName and gameID
        self.cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME=? AND GAMEID=?", (playerName, gameID))
        playerID_result = self.cursor.fetchone()
       
        if playerID_result is None:
            raise ValueError("Player not found")
        playerID = playerID_result[0]
        
        # Insert a new shot record
        self.cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID, gameID))
        self.conn.commit()
        
        # Return the new shotID
        return self.cursor.lastrowid
        

class Game:
    def __init__( self, gameID=None, gameName=None, player1Name=None,player2Name=None ):
        self.db =  Database()
        if gameID is not None:
            #gameID += 1
            gameName,player1Name,player2Name = self.db.getGame(gameID)

        else:
            gameID = self.db.setGame(gameName , player1Name , player2Name)
            
          
        self.gameID = gameID
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name 
        self.tableID = create_and_write_game_table(self.db) 


    def shoot(self, gameName, playerName, table, xvel, yvel):
        tables = []
        table_array = []
    # Get the shotID for the current game and player
        shotID = self.db.newShot(self.gameID, playerName)

    # Find the cue ball
        cue_ball = table.cueBall()
        
        if cue_ball is None:
            raise ValueError("Cue ball not found.")

    # Extract cue ball position
        posx = cue_ball.obj.still_ball.pos.x
        posy = cue_ball.obj.still_ball.pos.y

    # Set cue ball attributes
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel
        cue_ball.obj.rolling_ball.pos.x = posx
        cue_ball.obj.rolling_ball.pos.y = posy

    # Calculate acceleration
        speed = math.sqrt(xvel**2 + yvel**2)
        if speed > VEL_EPSILON:
            acc_x = -DRAG * xvel / speed
            acc_y = -DRAG * yvel / speed
        else:
            acc_x = acc_y = 0

        cue_ball.obj.number = 0  # Set cue ball number to 0
        cue_ball.obj.rolling_ball.acc.x = acc_x
        cue_ball.obj.rolling_ball.acc.y = acc_y

    

# Loop through segments
        current = table
        while table is not None:
            start = table.time
            current = table.segment()
            if current is None:
                break
            end = current.time
    # Calculate the duration from the start of the current segment to the start of the next
            
            if table is None:
                break
            segment_duration = end - start
    # Calculate the number of frames to simulate within this segment
            frame_count = int(segment_duration / FRAME_RATE)
           
    # Simulate each frame within the current segment
            for i in range(frame_count):
                current_time = i * FRAME_RATE
        # Use the original table to simulate rolling for the duration of the segment
                rolled_segment = table.roll(current_time)
                rolled_segment.time = start + current_time
                svg = rolled_segment.svg()
                #print(rolled_segment)  # Adjust the time accordingly
                table_array.append(svg)
                tables.append(rolled_segment)

        # Write the simulated state and record the shot
                segment_id = self.db.writeTable(rolled_segment,commit=False)
                self.tableID = segment_id
                self.db.recordTableShot(segment_id, shotID,commit=False)
            
            table = current

        if tables[len(tables) - 1].cueBall() is None:
            cue_ball_position = StillBall(0,Coordinate(1250 / 2, 2700 * 3 / 4))
            tables[len(tables) - 1 ] += cue_ball_position
            table_array.append(tables[len(tables)-1].svg())
            self.tableID =  self.db.writeTable(tables[len(tables) - 1])

        self.db.conn.commit()
        self.db.close()
        return table_array

def initialize_game_positions(BALL_DIAMETER=57.15):
   
    table_center_x = 1350 / 2
    foot_spot_y = 2700 / 4  
    
 
    apex_position = Coordinate(table_center_x, foot_spot_y)
    
 
    h_offset = BALL_DIAMETER
    v_offset = (3**0.5 / 2) * BALL_DIAMETER  
    
   
    ball_positions = [apex_position] 
    
  
    for row in range(1, 5): 
        for pos in range(row + 1):
            x = apex_position.x + (pos - row / 2.0) * h_offset
            y = apex_position.y - row * v_offset  
            ball_positions.append(Coordinate(x, y))
    
    
    cue_ball_position = Coordinate(table_center_x, 2700 * 3 / 4)  
    ball_positions.insert(0, cue_ball_position)  
    
    return ball_positions


def create_and_write_game_table(db):
    game_table = Table()
    

    ball_positions = initialize_game_positions()
    

    cue_ball = StillBall(0, ball_positions[0])  # Assuming 0 is the number for the cue ball
    game_table += cue_ball
    
 
    for i, position in enumerate(ball_positions[1:], start=1):
        ball_number = i if i < 8 else (i + 1 if i < 15 else 8)  # Adjust numbering to place the 8-ball in the center
        game_table += StillBall(ball_number, position)
   
    table_id = db.writeTable(game_table)

    return table_id 

def get_initial_game_state(db):
    print("get_initial_game_state called")
 
    initial_table_id = create_and_write_game_table(db)
  
    initial_table = db.readTable(initial_table_id )

    if initial_table is not None:
        
        svg_content = initial_table.svg()
        with open (f'table{initial_table_id}.svg','w') as f:
            f.write(svg_content)

        print(svg_content)
       # print(svg_content)
        return svg_content
    else:
        print("No initial game state found in the database")
        return "<!-- No initial game state found in the database -->"


if __name__ == "__main__":
    db = Database(reset=True)
    create_and_write_game_table(db)
