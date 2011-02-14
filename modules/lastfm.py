import ircbasic
import urllib2
import re
import pickle
import traceback
import sys
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
    url = "http://ws.audioscrobbler.com/1.0/user/" + user + "/recenttracks.rss"
    response = urllib2.urlopen(url)
    return response.read()

def getCur(user, g):
    m = re.search("(?<=/music/).*?(?=</link>)", g)
    m = m.group(0)
    m = urllib2.unquote(m)
    m = m.replace("/+noredirect/", "/")
    m = m.replace("+", " ")
    m = m.replace("&quot;", "\"")
    ct = m.replace("/_/", " - ")
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
            traceback.print_exc(file=sys.stdout)
            logError("lastfm2.py: " + origmsg)
            connection.sendMessage("AAAAA WHAT DID YOU DOOOOOOOO", channel)
            return False
    else:
        return False

def onChannelAction(connection, nick, channel, message, canTalk):
    return onChannelMode(connection, nick, channel, message, canTalk)

