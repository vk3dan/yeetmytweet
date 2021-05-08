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
                  access_token_secret=config.access_token_secret)

current_date = datetime.now()
daysago_date = current_date - timedelta(days=config.daysagotoyeet)
range_start = datetime.strptime('Mon Mar 20 00:00:00 +0000 2006','%a %b %d %H:%M:%S %z %Y')
range_end = datetime.strftime(daysago_date,'%a %b %d %H:%M:%S +0000 %Y')
helptext = """
    Usage: yeetmytweet.py <-i/-a>
           yeetmytweet.py <--interactive/--auto> 
    Options:
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
        opts, args = getopt.getopt(argv,"hia",['help','interactive','auto'])
    except getopt.GetoptError:
        print("ERROR: Unknown argument(s)")
        print(helptext)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(helptext)
            sys.exit()
#        elif opt in ("-u", "--username"):
#            if arg=="":
#                print("no username specified. Exiting")
#                sys.exit(5)
#            username = arg
#            print(f"Username: {username}")
        elif opt in ("-i", "--interactive"):
            print(f"This action will delete ALL tweets on your account created before : {datetime.strftime(daysago_date,'%b %d %Y')} ({config.daysagotoyeet} days ago).\n")
            print("THIS ACTION NOT BE UNDONE!\n")
            confirmation=input("Type YES to continue (not case sensitive): ")
            if confirmation.upper() != "YES":
                print("user failed to confirm destructive action. Exiting")
                sys.exit(4)
            else:
                print("user confirmed destructive action. Starting delete.")
        elif opt in ("-a", "--auto"):
            print(f"Automatic mode. This will delete ALL tweets on your account created before : {datetime.strftime(daysago_date,'%b %d %Y')} ({config.daysagotoyeet} days ago).\n")
            cancelsec=15
            try:
                while cancelsec:
                    print(f"You have {cancelsec} to press Ctrl-C to cancel the yeet ", end='\r')
                    time.sleep(1)
                    cancelsec -= 1
            except KeyboardInterrupt:
                print("\nOperation Cancelled by user before beginning.")
                sys.exit()
            print("Starting automatic delete.")
    yeeted=0
    while True:
        print(f"Yeeted {yeeted} tweets \r")
        ids=[]
        tweets = api.GetUserTimeline(api.VerifyCredentials().id, count=200, include_rts=True)
        for t in tweets:
            if t.created_at <= range_end:
                print(t.id)
                api.DestroyStatus(t.id)
                yeeted += 1
            if yeeted==0:
                print (f"All done, Exiting. Thanks for using yeetmytweet to yeet {yeeted} tweets")
                sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])