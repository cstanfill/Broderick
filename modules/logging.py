# we are using a fork of the HydraIRC logging scheme

import ircbasic
from ircbasic import *
import time # ...

### METHODS THAT SHOULD NOT BE IMPORTED ###
def logPrivmsg(source, contents):
    f="logs/prvtlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " ((prvt)) <" + source + "> " + contents + "\n")
    f.close()
    return False

def logPrivaction(source, contents):
    f="logs/prvtlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " ((prvt)) * " + source + " " + contents + "\n")
    f.close()
    return False
### END OF METHODS THAT SHOULD NTO BE IMPORTED ###

def onChannelMessage(connection, nick, channel, message, canTalk):
    if nick == channel:
        return logPrivmsg(nick, message)
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** <" + nick + "> " + message + "\n")
    f.close()
    return False

def onChannelAction(connection, nick, channel, message, canTalk):
    if nick == channel:
        return logPrivaction(nick, message)
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") * " + source + " " + contents + "\n")
    f.close()
    return False

def onChannelMode(connection, changer, channel, changed, extra, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** " + user + " sets channel mode " + mode + " " + argstring + "\n")
    f.close()
    return False

def onJoin(connection, nick, channel, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** " + nick + " (" + full + ") joined\n")
    f.close()
    return False

def onKick(connection, nick, channel, kicker, reason, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** " + nick + " was kicked by " + kicker + " (" + reason + ")\n")
    f.close()
    return False

def onPart(connection, nick, channel, reason, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** " + user + " has parted the channel (" + reason + ")\n")
    f.close()
    return False

def onNick(connection, oldnick, channel, newnick, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** " + oldnick + " changed nick to " + newnick + "\n")
    f.close()
    return False

def onBotJoin(connection, channel, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** now talking in this channel too\n")
    f.close()
    return False

def onBotPart(connection, channel, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftine("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") *** done talking in this channel\n")
    f.close()
    return False

def onBotNickChange(connection, newnick, canTalk):
    f="logs/chanlog.log"
    f = open(f, 'a')
    f.write(time.strftime("[%Y-%m-%d %H:%M:%S]") + " ((global)) *** changed nick to " + newnick + "\n")
    f.close()
    return False


### Import only this method ###
def logError(message, f="logs/errorlog.log"):
    f = open(f, 'a')
    message = time.strftime("[%Y-%m-%d %H:%M:%S]") + " ((error)) " + message
    if message[-1] != "\n":
        message = message + "\n"
    f.write(message)
    f.close()
    return False
