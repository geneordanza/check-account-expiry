#!/usr/bin/python
# DESC: Intershop users are warned upon logging into Xerox and Hubert servers
#       if their accounts are about to expire. Is it possible to add an email
#       alert notification to be delivered in the case where the user has not
#       logged into a server before it expires?
#
#       TICKET: C130055374

from datetime import date, datetime, timedelta
from calendar import month_abbr
from socket import gethostname

message = """
    System Notification
    ===================

    ACTION  : Password Reset
    HOSTNAME: %s
    LOGIN   : %s
    LAST PASSWORD CHANGED: %s
    NEXT PASSWORD CHANGED: %s
"""

def mailuser(*args):
    user, lastchg, nextchg = args[0], args[1], args[2]
    hostname = gethostname().upper()
    print '>> %s %s %s %s' % (user, lastchg, nextchg, hostname)


# Convert Unix timestamp into date object which is more user-friendly format
def convertTime(time):
    chgdate = datetime.fromtimestamp(time*60*60*24)
    chgdate = str(chgdate).split()[0]
    chgdate = chgdate.split('-')
    chgdate = map(int, chgdate)
    return date(chgdate[0], chgdate[1], chgdate[2])


# Extract the [1] username, [2] day warning for expiration, [3] last passwd change,
# [4] next passwd change.
def checkExpiry(line, today):
    user    = line.split(':')[0]
    maxdays = int(line.split(':')[4])
    warning = int(line.split(':')[5])
    lastchg = convertTime(float(line.split(':')[2]))
    nextchg = lastchg + timedelta(days=maxdays)
    diff    = nextchg - today

    if diff.days <= warning:
#       print user, lastchg, nextchg, diff.days
        mailuser(user, lastchg, nextchg)

def main():

    today  = date.today()
    filep  = open('/etc/shadow')

    for x in filep:
        passwd = x.split(':')[1]

        # Check if user has a valid password
        if passwd != '!!' and passwd != '*':
            checkExpiry(x, today)

    filep.close()

if  __name__ == '__main__':
    main()
