import socket
import re #Regular Expressions module
import time
import socket
import traceback
import sys
import irclib #Wrapper that allows simple calls for easy interfacing with the socket. Contains connection info as well.
import ircinterp #Interprets lines and notifies relevant modules, also does most of shell interface work
import threading
    
def shellInterface(event,connection) :
    rawData = ""
    interface = ircinterp.shinter(connection)
    while not event.isSet() :
        #Wait until we have a full new line, then evaluate it. Stop if we get the signal to end
        while (not "\n" in rawData) and not event.isSet() :
            rawData += sys.stdin.read(1)
        newLine = rawData.split("\n")[0]
        rawData = rawData.replace(newLine + "\n","",1)
        try :
	    exitCode = interface.interp(newLine)
            if exitCode == 1 :
                print "Reloading interface..."
                reload(ircinterp)
                interface = ircinterp.shinter(connection)
	    if exitCode == 2 :
		print "Quitting..."
		try : 
		    connection.sendLine("QUIT :Killed by console\r\n")
		    connection.conn.close()
		except : 
		    pass
		event.set()
        except :
            traceback.print_exc(file=sys.stdout)
            if newLine == "reload" :
                print "Reloading interface..."
                reload(ircinterp)
                interface = ircinterp.shinter(connection)
            else :
                print "Error encountered."
    
def runBot(network, server, port, nick, user, realname) :
    while True :
        if ircConnect(network, server, port, nick, user, realname) == 1 :
	    return
        time.sleep(1)
        
def ircConnect(network, server, port, nick, user, realname) :
    resetShell = threading.Event()
    resetShell.clear() #Make sure it is false
    try :
        #Set up a new socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server,6667))
        connection = irclib.ircPad(s, network, server, port, nick, user, realname)
        #Start up the shell interface thread
        shellThread = threading.Thread(target=shellInterface,args=(resetShell,connection,))
        shellThread.start()
        rawData = ""
        while not resetShell.isSet() :
            while not "\r\n" in rawData :
                rawData += s.recv(16)
            newLine = rawData.split("\r\n")[0]
            rawData = rawData.replace(newLine + "\r\n","",1)
            #Process line
            try :
                process(newLine, connection)
            except :
                #WHAT HAPPEN
                traceback.print_exc(file=sys.stdout)
        del(s)
        shellThread.join()
        del(shellThread)
	return 1 #This means "don't try to reconnect"
    except :
        #MAIN SCREEN TURN ON
        traceback.print_exc(file=sys.stdout)
	if resetShell.isSet() : #Indicates the problem was caused by the console closing the connection
            del(s)
            shellThread.join()
            del(shellThread)
	    return 1 #This means "don't try to reconnect"
        #Completely close socket
        s.close()
        del(s)
        #Kill shell interface and release thread
        resetShell.set()
        shellThread.join()
        del(shellThread)
        return 0 #This means we don't know what happened; try to reconnect.
    
def process(line, connection) :
    #Given line in plaintext, without \r\n at the end, as well as an ircpad instance
    #For each possible type of line, check if this is that kind of line; if so, evaluate as that, otherwise continue on
    for ltype in ircinterp.TYPES :
        matched= re.match(ltype[0], line)
        if matched :
            ltype[1](matched.groups(), connection, line) #Include the line in the function call in case it is needed
            return
    #Unidentified line type; print it out for future identification
    print "Could not identify this line: '%s'" % line
            
runBot("Foonetic","irc.foonetic.net",6667,"Brody","broderick","frozenGeek")
