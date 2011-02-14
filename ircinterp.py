import sys
global modulesLoaded
modulesLoaded = {}
global sortedModules
sortedModules = ()
def prnt(s) :
    f = open("logs/megalog.log","a")
    f.write(s + "\n")
class shinter :
    def __init__(self, connection) :
        self.connection = connection
        self.rawMode = False
        self.chatMode = False
	self.quitting = False
        print "Shell interface v4.13 initialized."
        sys.stdout.write("> ")
    def interp(self, newLine) :
        if self.rawMode : #Raw mode allows direct IRC commands to be entered. \x1b is the escape character.
            if newLine == '\x1b' :
                sys.stdout.write("Raw mode disabled\n")
                self.rawMode = False
            else :
                self.connection.sendLine(newLine)
        elif self.chatMode : #Chatmode functions as a very very basic IRC client. Should it be implemented in ircPad? \x1b is the escape character
            if newLine == '\x1b' :
                sys.stdout.write("Chat mode disabled\n")
                self.chatMode = False
            else :
                self.connection.sendLine(newLine)
        else : #Overview mode. Diagnostics and maintenance/administration.
            if newLine == "help" :
                sys.stdout.write("Commands available:\nrload - Reloads the ircinterp module\n")
                sys.stdout.write("raw - enters raw command execution mode\n")
                sys.stdout.write("chat - enters chat mode, a pseudo-client for IRC\n")
                sys.stdout.write("list - lists loaded modules\n")
		sys.stdout.write("load - loads a module by filename as the given internal name\n")
		sys.stdout.write("unload - unloads a module by the given internal name\n")
		sys.stdout.write("reload - reloads a module by given internal name, changing the internal name\n")
		sys.stdout.write("quit - gracefully leave IRC and exit program\n")
            elif newLine == "" :
                sys.stdout.write("==>\n")
            elif newLine == "rl" :
                return 1
            elif newLine == "raw" :
                sys.stdout.write("Raw mode enabled. Press ESC, then enter to leave\n")
                self.rawMode = True
            elif newLine == "chat" :
                sys.stdout.write("Chat mode enabled. Press ESC, then enter to leave\n")
                self.chatMode = True
            elif newLine == "list" :
                sys.stdout.write("Modules loaded: " + ", ".join(modulesLoaded.keys()) + "\n")
	    elif newLine.split(" ")[0] == 'load' :
		if importModule(newLine.split(" ")[1],newLine.split(" ")[2]) :
		    sys.stdout.write("Loaded module %s as %s.\n" % (newLine.split(" ")[1],newLine.split(" ")[2]))
		else : 
		    sys.stdout.write("Failed to load.\n")
	    elif newLine.split(" ")[0] == 'unload' :
		if unloadModule(newLine.split(" ")[1]) :
		    sys.stdout.write("Unloaded module %s.\n" % (newLine.split(" ")[1]))
		else :
		    sys.stdout.write("Failed to unload.\n")
	    elif newLine.split(" ")[0] == 'reload' : 
		if reloadModule(newLine.split(" ")[1],newLine.split(" ")[2]) :
		    sys.stdout.write("Reloaded %s as %s.\n" % (newLine.split(" ")[1],newLine.split(" ")[2]))
		else : 
		    sys.stdout.write("Failed to reload.\n")
	    elif newLine == "quit" :
		self.quitting = True
		sys.stdout.write("Are you sure you want to quit?\n")
	    elif self.quitting :
		if newLine == "exceedingly" :
		    sys.stdout.write("Okay! Goodbye.\n")
		    return 2 #Quit flag
		self.quitting = False
		sys.stdout.write("Okay. Disaster averted.\n")
            else :
                sys.stdout.write("That idea makes no sense and is basically meaningless.\n")
        sys.stdout.write("> ")
        return 0
    
def getModules() : #Get the modules in order of priority
    names = modulesLoaded.keys()
    modules = [modulesLoaded[name][0] for name in names]
    return sorted(modules, cmp=lambda a,b:cmp(b.PRIORITY,a.PRIORITY))

def importModule(filename, name) : #Load module modules/filename.py as name
    if name in modulesLoaded.keys() :
        return False #Name collision
    modulesLoaded[name] = ()
    exec("from modules import %s" % filename, globals())
    exec("reload(%s)" % filename)
    modulesLoaded[name] = (globals()[filename], filename)
    modulesLoaded[name][0].LOADNAME = name
    globals()['sortedModules'] = getModules()
    return True

def unloadModule(name) : #Remove whatever module was named name
    modulesLoaded = globals()['modulesLoaded']
    if not name in modulesLoaded.keys() :
        return False #Nonexistent module
    del(globals()[modulesLoaded[name][1]])
    del(modulesLoaded[name])
    return True

def reloadModule(oldname, newname) : #Reload the module named oldname, changing the name to newname.
    modulesLoaded = globals()['modulesLoaded']
    if not oldname in modulesLoaded.keys() :
        return False #Nonexistent module
    filename = modulesLoaded[oldname][1]
    unloadModule(oldname)
    importModule(filename, newname)
    return True

TYPES = []

def srvNotice(values, connection, line) :
    prnt("AUTH from %s of %s: %s" % (values[0],connection.network,values[1]))
    if values[1].find("Found your hostname") != -1 :
        #Server is ready for identification!    
        connection.sendUser(connection.username,connection.realname)
        connection.sendNick(connection.nickname)        
TYPES.append((":([^\.]+)\.[^ ]+ NOTICE AUTH :(.*)",srvNotice,"Server-level NOTICE"))

def srvInitMsg(values, connection, line) :
    identifier = int(values[1])
    prnt("MESSAGE from %s (of %s) no. %i: %s" % (values[0], connection.network, identifier, values[2]))
    if identifier == 332 :
        connection.setChanTopic(values[-1].split(" ")[0][1:], ":".join(values[-1].split(":")[1:]))
    if identifier == 353 :
        channel = values[-1].split("#")[1].split(" ")[0]
        names = values[-1].split(":")[1].replace("@","").replace("+","").replace("&","").replace("%","").split(" ")
        connection.setChanNicks(channel, names)        
TYPES.append((":([^\.]+).[^ ]+ ([0-9]{3}) [^ ]+ (.*)", srvInitMsg, "Server's initial 'hello' messages"))

def modeSetting(values, connection, line) :
    prnt("%s on %s set mode %s %s" % (values[0], connection.network, values[1], values[2]))
TYPES.append((":([^ ]+) MODE ([^ ]+) :(.*)",modeSetting,"Someone set a mode"))

def ping(values, connection, line) :
    prnt("Pinged on %s: '%s'" % (connection.network, values[0]))
    connection.sendLine("PONG " + values[0])    
TYPES.append(("PING (.*)",ping,"Someone pinged us"))

def privMsg(values, connection, line) :
    prnt("Privmsg on %s from %s: %s" % (connection.network, values[0], values[1])) 
    spoke = False   
    for module in sortedModules :
        spoke = spoke or module.onChannelMessage(connection,values[0],values[0],values[4], not spoke) 
TYPES.append((":([^\!]+)\!([^\@]+)\@([^ ]+) PRIVMSG ([^# ]+) :(.*)", privMsg,"Private message"))

def chanMsg(values, connection, line) :
    prnt("Chanmsg on %s%s from %s: %s" % (connection.network, values[3], values[0], values[4]))
    spoke = False
    for module in sortedModules :
        spoke = spoke or module.onChannelMessage(connection,values[0],values[3],values[4], not spoke)        
TYPES.append((":([^\!]+)\!([^\@]+)\@([^ ]+) PRIVMSG #([^ ]+) :(.*)", chanMsg,"Channel Message"))

def chanJoin(values, connection, line) :
    prnt("Join on %s%s by %s" % (connection.network, values[3], values[0]))
    connection.addChanNick(values[3],values[0])    
TYPES.append((":([^\!]+)\!([^\@]+)\@([^ ]+) JOIN :#(.*)",chanJoin, "Channel joined"))


