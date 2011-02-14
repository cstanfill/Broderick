# Here's my new convention, as per the file ../ModuleMethodConvention.txt
# modules import this and override where needed
# Added canTalk - only speak if no other modules have spoken yet.

def onChannelMessage(connection, nick, channel, message, canTalk):
    return False
def onChannelAction(connection, nick, channel, message, canTalk):
    return False
def onChannelMode(connection, changer, channel, changed, extra, canTalk):
    return False
def onJoin(connection, nick, channel, canTalk):
    return False
def onKick(connection, nick, channel, kicker, reason, canTalk):
    return False
def onPart(connection, nick, channel, reason, canTalk):
    return False
def onBotJoin(connection, channel, canTalk):
    return False
def onBotPart(connection, channel, canTalk):
    return False
def onBotNickChange(connection, newnick, canTalk):
    return False
LOADNAME = "" #changed when imported
PRIORITY = 0.0 #change in module?
