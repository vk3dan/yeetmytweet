#! /usr/bin/python3

import config, twitter, datetime, sys, getopt, time
from datetime import datetime, timedelta

"""
yeetmytweet
A python app to yeet old tweets into the bin.

Copyright 2021 Dan Phillips
"""

api = twitter.Api(consumer_key=config.consumer_key,
                  consumer_secret=config.consumer_secret,
                  access_token_key=config.access_token_key,
                  access_token_secret=config.access_token_secret,
                  sleep_on_rate_limit=True)

current_date = datetime.now()
daysago_date = current_date - timedelta(days=config.daysagotoyeet)
range_start = datetime.strptime('Mar 20 00:00:00 +0000 2006','%b %d %H:%M:%S %z %Y')
range_end = datetime.strftime(daysago_date,'%b %d %H:%M:%S %z %Y')
username=""
helptext = """
    Usage: yeetmytweet.py <-u someusername> <-i/-a>
           yeetmytweet.py <--username someusername> <--interactive/--auto> 
    Options:
        Note that order is important, username option MUST be first.
        -u (--username)    : Username         : (Followed by the username you are operating on)
        -i (--interactive) : Interactive mode : Asks for confirmation before deleting tweets
        -a (--auto)        : Automatic mode   : For use in a cronjob to automatically delete tweets
        -h (--help)        : Help             : Displays this help message
    any other options passed will be ignored and this message will be displayed.
    """
version= "0.1"

def main(argv):
    print(f"\nyeetmytweet version {version}. a python app to yeet old tweets into the bin.\n")
    if argv==[]:
        print("ERROR: No arguments given")
        print(helptext)
        sys.exit(1)
    try:
        opts, args = getopt.getopt(argv,"hu:ia",['help','username=','interactive','auto'])
    except getopt.GetoptError:
        print("ERROR: Unknown argument(s)")
        print(helptext)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(helptext)
            sys.exit()
        elif opt in ("-u", "--username"):
            if arg=="":
                print("no username specified. Exiting")
                sys.exit(5)
            username = arg
            print(f"Username: {username}")
        elif opt in ("-i", "--interactive"):
            print(f"This action will delete ALL tweets on account {username} created before : {datetime.strftime(daysago_date,'%b %d %Y')} (30 days ago).\n")
            print("THIS ACTION NOT BE UNDONE!\n")
            confirmation=input("Type YES to continue (not case sensitive): ")
            if confirmation.upper() != "YES":
                print("user failed to confirm destructive action. Exiting")
                sys.exit(4)
        elif opt in ("-a", "--auto"):
            print(f"Automatic mode. This will delete ALL tweets on account {username} created before : {datetime.strftime(daysago_date,'%b %d %Y')} (30 days ago).\n")
            cancelsec=10
            try:
                while cancelsec:
                    print(f"You have {cancelsec} to press Ctrl-C to cancel the yeet ", end='\r')
                    time.sleep(1)
                    cancelsec -= 1
            except KeyboardInterrupt:
                print("\nOperation Cancelled by user before beginning.")
                sys.exit()
            print("Starting automatic delete.")
        else:
            print("Invalid options. Exiting")
            sys.exit(6)

        
if __name__ == "__main__":
   main(sys.argv[1:])