class ircPad :
    conn = None
    def __init__(self, sock, network="", server="", port=0,nick="",user="",realname="") :
        self.conn = sock
        self.network = network
        self.server = server
        self.port = port
        self.nickname = nick
        self.username = user
        self.realname = realname
        self.channels = {}
    def getChanNicks(self, channame) :
        if channame in self.channels.keys() :
            return self.channels[channame][0]
        return []
    def setChanNicks(self, channame, names) :
        if not channame in self.channels.keys() :
            self.channels[channame] = [[],""]
        self.channels[channame][0]= names
    def addChanNick(self, channame, user) :
        if not channame in self.channels.keys() :
            self.channels[channame] = [[],""]
        self.channels[channame][0].append(user)
    def delChanNick(self, channame, user) :
        if channame in self.channels.keys() :
            if user in self.channels[channame][0] :
                self.channels[channame][0].remove(user)
    def setChanTopic(self, channame, topic) :
        if not channame in self.channels.keys() :
            self.channels[channame] = [[],""]
        self.channels[channame][1] = topic
    def sendLine(self, line) :
        self.conn.send(line.strip("\r\n") + "\r\n")
    def sendUser(self, user, realname) :
        self.sendLine("USER " + user + " 0 * :" + realname)
    def sendNick(self, nick) :
        self.sendLine("NICK " + nick)
    def sendOper(self, name, password) :
        self.sendLine("OPER " + name + " " + password)
    def sendMode(self, nick, mode) :
        self.sendLine("MODE " + nick + " " + mode)
    def sendQuit(self, message="") :
        self.sendLine("QUIT :" + message)
    def joinChannel(self, channel, key="") :
        self.sendLine("JOIN " + "#" + channel + " " + key)
    def partChannel(self, channel, message="") :
        self.sendLine("PART " + "#" + channel + " :" + message)
    def sendChannelMode(self, channel, mode) :
        self.sendLine("MODE " + "#" + channel + " " + mode)
    def setTopic(self, channel, topic="") :
        self.sendLine("TOPIC " + "#" + channel + " :" + topic)
    def getTopic(self, channel) :
        self.sendLine("TOPIC " + "#" + channel)
    def inviteUser(self, nick, channel) :
        self.sendLine("INVITE " + nick + " " + "#" + channel)
    def kickUser(self, channel, user, reason="") :
        self.sendLine("KICK " + "#" + channel + " " + user + " :" + reason)
    def sendMessage(self, mess, target) :
        self.sendLine("PRIVMSG " + "#" + target + " :" + mess)
        print "< " + self.nickname + "> " + target + "\t" + mess
    def sendNotice(self, target, message) :
        self.sendLine("NOTICE " + target + " :" + mess)
    def goAway(self, message = "") :
        self.sendLine("AWAY :" + message)
    def ban(self, user, chan) :
        self.sendChanMode(chan, "+b " + user)
    def voice(self, user, chan) :
        self.sendChanMode(chan, "+v " + user)
    def mute(self, user, chan) :
        self.sendChanMode(chan, "-v " + user)
