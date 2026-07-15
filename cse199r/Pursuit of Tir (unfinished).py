# """This copy is for adding time variation to the coordinate system"""

# """update locations with ids"""

# """update coordinate system to have a universal scale (or built in scale)""" (pretty sure this is done)
"""update position coordinate system to not be by minutes"""

"""creating actual map locations and implimenting a location connection discovery system - """

"""switch location indeces with dictionaries that use the location name (or a code) as the key for the value which is the location object itself"""
# """switch option_indeces to dictionaries (?)"""

"""Add paths (position level routes to undiscovered locations/positions(?)) and junctions (location level intermediate areas that have *paths to undiscovered locations)"""

"""prototype events system"""

# """change global variables to object [class] properties"""

"""incorporate the text display program"""

"""Fix text-centering for more intuitive use"""

""" --- NEXT ITERATION: replace current_ variables with class properties (class player: player.location, .region, etc.) --- """


from random import choice,randint
from math import sqrt
from os import system
from full_screen_display import screen
from coord import compass


if True:
    # index constants:
    HOURS_INDEX = 0
    MINUTES_INDEX = 1
    AMPM_INDEX = 2
    TIME_OF_DAY_INDEX = 3

    WEATHER_CODE_INDEX = 0
    WEATHER_START_DAY_INDEX = 1

    Y_COORD_INDEX = 0
    X_COORD_INDEX = 1

    VALID_CHECK_INDEX = 0
    TARGET_REGION_INDEX = 1
    TARGET_LOCATION_INDEX = 2

    ACTION_LABEL_INDEX = 0
    ACTION_TYPE_INDEX = 1

    WEATHER_CHANCE_INDEX = 0
    WEATHER_DIVISION_INDEX = 1
    WEATHER_TYPE_INDEX = 0
    WEATHER_CHANGE_INDEX = 1

    LOCATION_DISTANCE_SCALE = 5

    # find unused functions in previous versions

if True:
    # program window parameters
    SCREEN_WIDTH = 130
    SCREEN_HEIGHT = 30

    system(f'mode con: cols={SCREEN_WIDTH} lines={SCREEN_HEIGHT}')

    TERMINAL_WIDTH = 100
    SCREEN_MARGIN = int((SCREEN_WIDTH - TERMINAL_WIDTH) / 2)

class g:
    time = [5,0,"PM","d"]
    weather = ["c",0]
    day_count = 1

def cycle_weather():
    """Pass no arguments"""
    
    if current_location.weather != "":
        weather = current_location.weather
    else:
        weather = current_region.weather

    new = randint(1,100)
    if new in range(1,weather[WEATHER_CHANCE_INDEX]):
        new = randint(1,100)
        for v in weather[WEATHER_DIVISION_INDEX]:
            if new in range(v[WEATHER_CHANGE_INDEX]):
                if v[WEATHER_CODE_INDEX] == "f" and g.time[TIME_OF_DAY_INDEX] == "d":
                    new_weather = weather[WEATHER_DIVISION_INDEX][(weather[WEATHER_DIVISION_INDEX].index(v) - 1)][WEATHER_CODE_INDEX]
                else:
                    new_weather = v[WEATHER_CODE_INDEX]
                break
    else:
        new_weather = "c"
    g.weather = [new_weather,g.day_count]

def return_weather():
    # Weather Codes: r - rain ; s - snow ; f - fog ; d - deep fog ; c - clear sky ; w - wind
    if g.weather[WEATHER_CODE_INDEX] == "c":
        current_weather = "Clear Sky"
    elif g.weather[WEATHER_CODE_INDEX] == "r":
        current_weather = "Raining"
    elif g.weather[WEATHER_CODE_INDEX] == "s":
        current_weather = "Snowing"
    elif g.weather[WEATHER_CODE_INDEX] == "f" or g.weather[WEATHER_CODE_INDEX] == "d":
        current_weather = "Fog"
    elif g.weather[WEATHER_CODE_INDEX] == "w":
        current_weather = "High Winds"
    else:
        current_weather = ["<<Weather Code Error>>",g.weather[WEATHER_CODE_INDEX]]
    return current_weather

def return_header():
    return f" `@ Day {str(g.day_count)} | {return_time()} | {return_weather()} `^ {current_location.name} {current_position.name} `^^ `@ "
    


def ampm_switch ():
    g.time[AMPM_INDEX] = "PM" if g.time[AMPM_INDEX].lower() == "am" else "AM"
    g.day_count += 1 if g.time[AMPM_INDEX].lower() == "am" else 0
    

def true_coord(reg_coord,loc_coord):
    y = reg_coord[Y_COORD_INDEX] + round(loc_coord[Y_COORD_INDEX] / LOCATION_DISTANCE_SCALE)
    x = reg_coord[X_COORD_INDEX] + round(loc_coord[X_COORD_INDEX] / LOCATION_DISTANCE_SCALE)
    return [y,x]
    

def calc_time(new,old,scale):
    """New Coordinates, Old Coordinates, Scale"""

    distance = calc_distance(new,old)
    if scale == "l":
        distance = distance / LOCATION_DISTANCE_SCALE
    if scale in "rl":
        time = round(distance / 4 * 60)     # 4 to be replaced with travel speed variable
        pick_time = choice(range(round(time * .85 * 1000),round(time * 1.15 * 1000)))
        hours = (pick_time / 1000) // 60
        minutes = (pick_time / 1000) % 60
        pass_time(hours,minutes)
    if scale == "p":
        pass_time(0,choice(range(round(distance*.85),round(distance * 1.15))))


def calc_distance(new_coord,old_coord):
    """New Coordinates, Old Coordinates"""
    distance = sqrt((old_coord[Y_COORD_INDEX] - new_coord[Y_COORD_INDEX]) ** 2 + (old_coord[X_COORD_INDEX] - new_coord[X_COORD_INDEX]) ** 2)
    return round(distance,2)

def pass_time (hours,minutes, days=0):
    """Hours, minutes, (days=0) - hours/minutes will not advance if days != 0"""
    
    if days != 0:
        g.day_count += days
        g.time = [10,0,"AM","d"]
        
    else:
        current_hours = g.time[HOURS_INDEX] if g.time[HOURS_INDEX] != 12 else 0
        current_minutes = g.time[MINUTES_INDEX]
        weather_time = 1.2 if g.weather[WEATHER_CODE_INDEX] in "rs" else 1
        night_time = 1.2 if g.time[TIME_OF_DAY_INDEX] == "n" else 1
        add_minutes = round(minutes * weather_time * night_time + current_minutes)
        add_hours = round(hours * weather_time * night_time + current_hours)
        while add_minutes > 59:
            add_minutes -= 60
            add_hours += 1
        while add_hours > 11:
            add_hours -= 12
            ampm_switch()

        if add_hours >= 9 and g.time[AMPM_INDEX].lower() == "pm":
            time_of_day = "n"
        elif add_hours < 5 and g.time[AMPM_INDEX].lower() == "am":
            time_of_day = "n"
        elif 5 <= add_hours < 7 and g.time[AMPM_INDEX].lower() == "am":
            time_of_day = "m"
        elif 7 <= add_hours < 9 and g.time[AMPM_INDEX].lower() == "pm":
            time_of_day = "e"
        else:
            time_of_day = "d"

        g.time = [add_hours if add_hours != 0 else 12 ,add_minutes,g.time[AMPM_INDEX],time_of_day]

def return_time():

    hours = f"{g.time[HOURS_INDEX]}"
    
    if len(str(g.time[MINUTES_INDEX])) == 1:
        minutes = f"0{g.time[MINUTES_INDEX]}"
    else:
        minutes = f"{g.time[MINUTES_INDEX]}"
    
    return f"{hours}:{minutes} {g.time[AMPM_INDEX]}"


class event:
    index = []

    def __init__ (self,id,name):
        self.id = id
        self.name = name

        event.index.append(self)

class position:
    index = []
    all = {}
    option_index = []

    def __init__ (self,id,name,location,descriptions,connections,coord,events,visited=0,hidden=0,locked=0,shelter=0,egress_valid=1,disc=1,path=0):
        """Name, Location, Descriptions, Connections "code string", Coordinates [Y,X] (in minutes), Events"""
        self.id = id
        self.name = name
        self.location = location
        self.descriptions = descriptions
        self.connections = connections      # string - includes own code as well as code of all connected locations
        self.events = events
        self.coord = coord
        self.hidden = hidden
        self.locked = locked
        self.shelter = shelter
        self.visited = visited
        self.egress_valid = egress_valid
        self.disc = disc
        self.path = path

        self.choose_position = []

        position.index.append(self)
        try:
            assert id in position.all
            input("ID already used")
        except:
            position.all[id] = self

class location:
    index = []      # this is a list of objects, which each have attributes which must be specifically called
    all = {}        # this is a set of objects with an id as key
    option_index = []

    def __init__(self,id,name,region,descriptions,code,connections,coord,events,weather="",visited=0,hidden=0,locked=0,egress_valid=[0,"",""],disc=0,outskirts="Outskirts",outdesc="outskirts",outcoord=[0,0]):
        """Name, Region, Descriptions, Location Code "string", Connections "string", Coordinates [Y,X] in 1/2 miles, Events"""
        self.id = id
        self.name = name
        self.region = region
        self.descriptions = descriptions
        self.code = code
        self.connections = connections      # string - includes own code as well as code of all connected locations
        self.events = events
        self.coord = coord
        self.weather=weather
        self.hidden = hidden
        self.locked = locked
        self.visited = visited
        self.egress_valid = egress_valid
        self.disc = disc

        self.choose_location = []

        # outidget = name
        outid = id + "out"
        
            # outid += v[0]
        self.outskirts = position(outid,outskirts,id,outdesc,"1",outcoord,None)

        location.index.append(self)
        try:
            assert id in location.all
            input("ID already used")
        except:
            location.all[id] = self

class region:
    index = []
    all = {}
    option_index = []

    def __init__(self,id,name,descriptions,code,transit,coord,events,weather=[10,[["d",5],["r",75],["f",100]]],visited=0,hidden=0,locked=0):
        """Name, Descriptions, Region Code, Connections [(code, location obj, distance range) , ...], Coordinates [Y,X] in miles), Events"""
        self.id = id
        self.name = name
        self.descriptions = descriptions
        self.code = code
        self.transit = transit
        self.events = events
        self.coord = coord
        self.weather = weather
        self.visited = visited
        self.hidden = hidden
        self.locked = locked
        
        self.adjacent = ""
        if transit != None:                 # |
            for v in transit:               # | currently obsolete
                self.adjacent += v[0]       # |

        region.index.append(self)
        try:
            assert id in region.all
            input("ID already used")
        except:
            region.all[id] = self

def preload():

    # generate map objects
    
    #lampetts (new)

    desc = "<descriptions here>"
    ev = ""

    location("lplh","Louston Homestead","lp","The homestead sits in a swath of wide fields, nestled against a small grove of trees.","a","123c",[0,0],ev,hidden=0,outskirts="Property Gate",outcoord=[6,8],disc=1)
    if True:
        position("lhlh","Lodging House","lplh",desc,"1",[0,0],ev)
        position("lhrh","Ranch House","lplh",desc,"1",[2,2],ev)
        position("lhs","Stable","lplh",desc,"1",[1,-2],ev)
        position("lhch","Cook House","lplh",desc,'1',[0,1],ev)
        position("lho","Orchard","lplh",desc,"12",[-5,5],ev)
        position("lhpt","an overgrown trail...","lplh",desc,"2",[-8,2],ev)

    location("lplr","Louston Ranch","lp",desc,"1","a23c",[3,11],ev,hidden=0,outskirts="Crossroads",disc=1)
    # if True:
    #     position("North Pasture")
    #     position("Corrals")
    #     position("")
    location("lpd","Dawson","lp",desc,"2","13c",[14,32],ev,hidden=0,outskirts="Main Street",disc=1)
    location("lpm","Dawson Coal Mine","lp",desc,"c","215",[12,-24],ev,hidden=0,disc=1)
    location("lpj","Jonaston","lp",desc,"3","12",[99,57],ev,hidden=0,outskirts="Main Road",disc=1)
    
    region("lp","Lampetts Praire",desc,"1",[],[0,0],ev)
    
    
    location("nltl","Tas Laramo","nl",desc,"1","sf2",[0,0],ev,hidden=0,outskirts="City Outskirts",outcoord=[-20,-20],disc=1)
    location("nlps","Port Sulphur","nl",desc,"s","1f",[0,2],ev,hidden=1,outskirts="Gull Street")
    location("nlpf","Port Ferrgula","nl",desc,"f","1s",[3,0],ev,hidden=0,outskirts="Docks",disc=1)
    location("nlit","Ilen Town","nl",desc,"2","1",[43,-26],ev,hidden=0,outcoord=[-5,-5],disc=1)
    
    region("nl","Newman's Landing",desc,"0",[],[94,52],ev)


    if True:    # enable region connections
        # find_loc("Jonaston","Lampetts Praire").egress_valid = [1,find_reg("Newman's Landing"),find_loc("Tas Laramo", "Newman's Landing")]
        location.all["lpj"].egress_valid = [1,region.all["nl"],location.all["nltl"]]
        find_loc("nltl","nl").egress_valid = [1,find_reg("lp"),find_loc("lpj","lp")]

    if False:
        #lampetts

        orlends_barn = position("Barn","Orlends",["old barn","creaky barn"],"1",None)
        orlends_field = position("Field","Orlends",["field","cornfield"],"1",None)
        orlends_bank = position("Bank","Orlends",["brickwork bank","First Bank"],"1",None)

        ubalts_peak = position("Peak","Ubalts",["windy mountain","expedition site"],"a",None)
        ubalts_woods = position("Woods","Ubalts",["pine forest","burnt forest"],"1",None)
        ubalts_river = position("River","Ubalts",["rapid river","cold river"],"1a",None)

        prag_clearing = position("Clearing","Prag",["clearing in forest","old logging operation"],"1",None)
        prag_farm = position("Farm","Prag",["abandoned farm","barley farm"],"1",None)
        prag_mine = position("Mine","Prag",["old mine","silver mine"],"1",None)


        lampetts_orlends = location("Orlends","Lampetts Praire","city","1","23",None,range(2,10),outskirts="Main Street",weather=[85,[["d",5],["r",85],["f",100]]])
        ubalts_desc = ["mountains morning",("mountains day","mountains first visit day","mountains rain day"),"mountains evening",("mountains night","mountains first visit night","mountains rain night")]
        lampetts_ubalts = location("Ubalts","Lampetts Praire","mountains","2","13",None,range(5,16),weather=[20,[["d",5],["r",35],["s",65],["f",100]]])
        lampetts_prag = location("Prag","Lampetts Praire","forest","3","12",None,range(10,21),weather=[30,[["r",50],["w",95],["f",100]]])

        #tambia

        tambia_woods = location("Woods","Tambia","deciduous forest","1","23",None,range(7,17))
        tambia_baski = location("Baski City","Tambia","city","2","13",None,range(1,6))
        tambia_bridge = location("Polenta Bridge","Tambia","bridge","3","124",None,range(2,14))

        #ederas

        ederas_pass = location("Pass","The Ederas","mountain pass","3","1245",None,range(5,15))
        ederas_mt_nelen = location("Mt. Nelen","The Ederas","mountainside","1","23",None,range(5,13))
        ederas_mt_trask = location("Mt. Trask","The Ederas","mountainside","2","13",None,range(10,26))
        ederas_mt_rubell = location("Mt. Rubell","The Ederas","mountainside","4","34",None,range(3,10))
        ederas_mt_josephine = location("Mt. Josephine","The Ederas","mountainside","5","34",None,range(5,12))

        # regions
        lampetts = region("Lampetts Praire","Wide grasslands","1",[("2",lampetts_orlends, range(12,30)),("3",lampetts_ubalts,range(19,37))],None,range(6,10))
        tambia = region("Tambia","Lowland forests","2",[("1",tambia_woods, range(12,30)),("3",tambia_baski,range(13,31))],None,range(8,12))
        ederas = region("The Ederas","mountain range","3",[("1",ederas_mt_nelen,range(19,37)),("2",ederas_mt_josephine,range(13,31))],None,range(8,14))
    null_region = region("null",None,None,None,None,None,None)

    # preload position connections from sets

    for v in position.all:
        position_options = []
        for c in position.all:
            if v != c and pos(v).location == pos(c).location:
                for i in list(pos(v).connections):
                    if i in pos(c).connections:
                        position_options.append(c)
                        break
        pos(v).choose_position = position_options
        position.option_index.append(position_options)


    # preload location connections from sets

    for v in location.all:
        location_options = []
        for c in location.all:
            if v != c and loc(v).region == loc(c).region:
                # for i in list(location.all[v].connections):
                if loc(c).code in loc(v).connections:
                    location_options.append(c)
        loc(v).choose_location = location_options
        location.option_index.append(location_options)

    # for v in location.all:
    #     print (  map(lambda x: x.name,map(loc,loc(v).choose_location))  )
    #     print (list(  map(lambda x: x.name,map(loc,loc(v).choose_location))  ))
    
    # preload region connections - currently obsolete (?)

    for v in region.index:
        region_options = []
        for c in region.index:
            if c.code in list(v.adjacent) and c != v and v != null_region:
                region_options.append(c)
        v.choose_region = region_options
        region.option_index.append(region_options)

    # preload region connections from sets
    # currently obsolete
    
    return (loc("lpj"),loc("lpj").outskirts,reg("lp"),null_region)


    # # Verify
    # print(len(region.option_index))
    # for v in region.index:
    #     for i in v.choose_region:
    #         print(v.name,i.name, sep = ", ")


def pos(id):
    """Returns object from position.all"""
    return position.all[id]

def loc(id):
    """Returns object from location.all"""
    return location.all[id]

def reg(id):
    """Returns object from region.all"""
    return region.all[id]

def find_pos(id, location):
    """Position ID, Location ID - returns position object"""
    for v in position.index:
        if v.id == id and v.location == location:
            return v
    input("Error: position not found.")

def find_loc(id, region):
    """Location ID, Region ID - returns location object"""

    for v in location.index:
        if v.id == id and v.region == region:
            return v
    input("Error: location not found.")

def find_reg(id):
    """Region ID - returns region object"""
    for v in region.index:
        if v.id == id:
            return v
    input("Error: region not found.")

start_data = preload()
current_location, current_position, current_region, null_region = start_data





action_options = []
last_action = "change_location"
option = -1
while True:
    

    text = return_header()
    if option - 1 >= 0:
        if last_action == "change_location":
            text += f" `^ {current_location.descriptions}  `^"
            text += f" `^ {current_position.descriptions}  `^"
        elif last_action == "change_position":
            text += f" `^ {current_position.descriptions}  `^"
        elif last_action == "change_region":
            text += f" `^ {current_region.descriptions}  `^"
            text += f" `^ {current_location.descriptions}  `^"
        text += " `^ "


    if True:
        action_options = []
        if current_position.choose_position != []:
            action_options.append(["Move","change_position"])
        if current_position.egress_valid == 1 and current_location.choose_location != []:
            action_options.append([f"Leave {current_location.name}","change_location"])
        if current_location.egress_valid[VALID_CHECK_INDEX] == 1:
            action_options.append([f"Trek to {current_location.egress_valid[TARGET_REGION_INDEX].name}","change_region"])
        

    for i,v in enumerate(action_options):
        text += f" `_8 {i+1} - {v[ACTION_LABEL_INDEX]} `^ "
    er = 0
    while True:
        screen(text)
        try:
            option = int(input(">>>> "))
            assert 0 < option <= len(action_options)
            break
        except:
            if er == 0:
                text += " `^ `@  <<Please enter a number within the given range>> `^ `@ "
                er = 1

    if action_options[option - 1][ACTION_TYPE_INDEX] == "change_location":
        last_action = "change_location"
        
        text = return_header()
        text += " Where do you want to go? `^^ "

        choose_list = []
        locked_list = []
        name_len = 0
        for v in current_location.choose_location:
            if loc(v).hidden == 0:
                if len(loc(v).name) > name_len:
                    name_len = len(loc(v).name)
                if loc(v).locked != 1:
                    choose_list.append(loc(v))
                else:
                    locked_list.append(loc(v))

        for i,v in enumerate(choose_list):
            temp_distance = round(calc_distance(v.coord,current_location.coord) / LOCATION_DISTANCE_SCALE)
            if v.visited == 0:
                text += f" `_8 {i+1} - {v.name}: {"`" + "_" + str(name_len + 2 - len(v.name))} {temp_distance} miles {compass(v.coord,current_location.coord)} `^ "
            else:
                text += f" `_8 {i+1} - {v.name} - (visited): {"`" + "_" + str(name_len + 2 - len(v.name))} {temp_distance} miles {compass(v.coord,current_location.coord)} `^ "
        for v in locked_list:
            temp_distance = round(calc_distance(v.coord,current_location.coord) / LOCATION_DISTANCE_SCALE)
            if v.visited == 0:
                text += f" `_8 X - {v.name}: {"`" + "_" + str(name_len + 2 - len(v.name))} {temp_distance} miles {compass(v.coord,current_location.coord)} `^ " 
            else:
                text += f" `_8 X - {v.name} - (visited): {"`" + "_" + str(name_len + 2 - len(v.name))} {temp_distance} miles {compass(v.coord,current_location.coord)} `^ "
        text += f" `_8 0 - Cancel `^^ "
        screen(text)
        option = int(input(">>>> "))
        if option == 0:
            pass
        else:
            calc_time(choose_list[option - 1].coord,current_location.coord,"l")
            current_location = choose_list[option - 1]
            current_position = current_location.outskirts
            cycle_weather()

    elif action_options[option - 1][ACTION_TYPE_INDEX] == 'change_position':
        last_action = "change_position"
        text = return_header()
        text += " Where would you like to move? `^^ "
        
        choose_list = []
        locked_list = []
        for v in current_position.choose_position:
            if pos(v).hidden == 0:
                if pos(v).locked != 1:
                    choose_list.append(pos(v))
                else:
                    locked_list.append(pos(v))

        for i,v in enumerate(choose_list):
            text += f" `_8 {i+1} - {v.name} `^ " if v.visited == 0 else f" `_8 {i+1} - {v.name} - (visited) `^ "
        for v in locked_list:
            text += f" `_8 X - {v.name} `^ " if v.visited == 0 else f" `_8 X - {v.name} - (visited) `^ "
        text += f" `_8 0 - Cancel `^^ "
        screen(text)
        option = int(input(">>>> "))
        if option == 0:
            pass
        else:
            calc_time(choose_list[option - 1].coord,current_position.coord,"p")
            current_position = choose_list[option - 1]

    elif action_options[option - 1][ACTION_TYPE_INDEX] == 'change_region':
        last_action = "change_region"

        target_region = current_location.egress_valid[TARGET_REGION_INDEX]
        target_location = current_location.egress_valid[TARGET_LOCATION_INDEX]
        calc_time(true_coord(target_region.coord,target_location.coord),true_coord(current_region.coord,current_location.coord),"r")
        current_region = target_region
        current_location = target_location
        current_position = current_location.outskirts
        cycle_weather()
        target_region = null_region