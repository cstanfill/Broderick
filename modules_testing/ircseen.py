import time #...
import re

chans = dict() # this structure requires some explanation.  It's a dictionary, 
# obviously.  Each of the entries takes a channel name that the bot is in as a key, 
# and the value returned is...another dictionary.  The returned dictionary takes as a 
# key the name of a user who is in / was in the channel, and returns some information 
# about what they did last night.

def onChannelMessage(connection, nick, channel, message, canTalk):
    try:
        talked = False
        if nick == channel:
            # the user is being an idiot and querying in private
            return False
        if message[:6] = "!seen " and canTalk:
            # the command for a !seen query has been tripped
            # as a side note, this should also be logged
            # and be sure not to modify message
            talked = True
            try:
                target = message.split(" ", 1)[1]
                try:
                    # database lookup
                    thischannel = chans[channel]
                    str = thischannel[target]
                    str = nick + ": " + target + str
                    connection.sendMessage(str, channel)
                except:
                    # chanlog parse
                    try:
                        # actually parse the chanlog
                        bl = "../logs/chanlog.log"
                        logf = open(bl, "r")
                        regexp = "\[[^\n]*]\ (" + channel + ") *** <" + target + "> [^\n]*(?!.*<" + target + ">)"
                        m = re.search(regexp, logf, re.DOTALL)
                        logf.close()
                        m = m.group(0)
                        year = re.search("(?<=\[).*?(?=-)", m).group(0)
                        pmonth = re.search("(?<=-).*?(?=-)", m).group(0)
                        if pmonth == "01":
                            month = "January"
                        elif pmonth == "02":
                            month = "February"
                        elif pmonth == "03":
                            month = "March"
                        elif pmonth == "04":
                            month = "April"
                        elif pmonth == "05":
                            month = "May"
                        elif pmonth == "06":
                            month = "June"
                        elif pmonth == "07":
                            # it's the month of July
                            month == "July"
                        elif pmonth == "08":
                            month = "August"
                        elif pmonth == "09":
                            month = "September"
                        elif pmonth == "10":
                            month = "October"
                        elif pmonth == "11":
                            month = "November"
                        elif pmonth = "12":
                            month = "December"
                        else:
                            month = "OH GOD WHAT HAPPEN"
                        day = re.search("(?<=-)[0-9]*?(?= )", m).group(0)
                        if day[-1] == "1":
                            day = day + "st"
                        elif day[-1] == "2":
                            day = day + "nd"
                        elif day[-1] == "3":
                            day = day + "rd"
                        else:
                            day = day + "th"
                        hour = int(re.search("(?<= ).*?(?=:)", m).group(0))
                        pm = 0
                        if hour > 11:
                            pm = 1
                            hour = hour - 12
                        if hour <= 0:
                            hour = 12
                        hour = str(hour)
                        minute = re.search("(?<=:).*?(?=:)", m).group(0)
                        if pm == 1:
                            pm = "PM"
                        elif pm == 0:
                            pm = "AM"
                        else:
                            pm = "OH GOD WHAT HAPPEN"
                        # seconds = re.search("(?<=:)[0-9].*?(?=\])", m).group(0)
                        msg = re.search("(?<=> ).*", m).group(0)
                        str = nick + ": " + target + ", on " + month + " " + day + ", " + year + " at (E(S/DS)T) " + hour + ":" + minute + " " + PM + ", said: \"" + msg "\"."
                        connection.sendMessage(str, channel)
                    except:
                        # nothing in the chanlog
                        connection.sendMessage(nick + ": Never hoid of 'em.")
                        talked = True
            except:
                talked = false
        # out here, at this indentation level, do logging
        # let logging.py take care of logging and we'll update chans[channel]:
        try:
            thischannel = chans[channel]
        except:
            # it doesn't exist, so let's make it
            chans[channel] = dict()
            thischannel = chans[channel]
        # come up with string:
        record = time.strftime(", on %B %d, %Y at (E(D/DS)T) %I:%M %p, said: \"") + message + "\"."
        # save it
        thischannel[nick] = record
        return talked
    except:
        return False
# end of [onChannelMessage]
