import ircbasic
import urllib2
import re
import pickle
from logging import logError

def lookupUser(nick):
    f = "../rsrc/lastfm.dict"
    f = open(f, 'r')
    bill = pickle.load(f) # bill is a dict
    user = bill[nick]
    f.close()
    return user

def setUser(nick, user):
    f = "../rsrc/lastfm.dict"
    fl = open(f, 'r')
    bill = pickle.load(fl) # bill is a dict
    bill[nick] = user
    fl.close()
    fe = open(f, 'w')
    pickle.dump(bill, fe)
    fe.close()
    return lookupUser(nick)

def loadUrl(user):
    url = "http//last.fm/user/" + user
    response = urllib2.urlopen(url)
    g = response.read()
    g = g.replace("/+noredirect/", "/")
    return g

def getCur(user, g):
    m = re.search("(?<=href=\"/music/).*?(?=\">)", g)
    m = m.group(0)
    m = urllib2.unquote(m)
    m = m.replace("+", " ")
    m = m.replace("&quot;", "\"")
    ma = re.match(".*?(?=\/)", m)
    mt = re.search("(?<=\/\_\/).*", m)
    ma = ma.group(0)
    mt = mt.group(0)
    ct = ma + " - " + mt
    return ct

# def getPrev(user, g): # to be implemented later (needs moar regexps / me actually feeling like looking at html output)

def onChannelMessage(connection, nick, channel, message, canTalk):
    if canTalk:
        try:
            origmsg = message
            if message[:3] == "!np" or message[:3] == "!fm" or message[:2] == "np" or message[:2] == "fm":
                # we'll do shit
                try:
                    # and hope nothing goes wrong
                    message = message.split(" ", 1)[1] # split out !np or !fm
                    if len(message) >= 4 and message[:4] == "set ":
                        message = message.split(" ", 1)
                        user = message[1] # keep this seperate; don't rememeber why
                        user = setUser(nick, user)
                    else:
                        user = message
                except:
                    user = lookupUser(nick)
                urlload = loadUrl(user)
                cur = getCur(user, urlload)
                # todo: make this a better string
                # but for now
                msg = cur
                connection.sendMessage(msg, channel)
                return True
            else:
                # we're not fecalpheliacs today, sorry
                return False
        except:
            # no idea what happened
            logging.logError("lastfm.py: " + origmsg)
            connection.sendMessage("AAAAA WHAT DID YOU DOOOOOOOOOO", channel)
            return False
    else:
        return False

def onChannelAction(connection, nick, channel, message, canTalk):
    return onChannelMode(connection, nick, channel, message, canTalk)

