import time
import pollAndPlace
import textUpdates
import cConfig

#create the config dict
config =cConfig.readConfig()
#global variables
masterLock =True
keywords=['bigRestart']
passes=0
polls=0
pingsT=0
suspend = False

#flip-flop for suspend
def flop():
    global suspend
    suspend=not suspend
#try to text theuser and handle the scenario when there is no internet
def tryTextUser(text):
    try:
        textUpdates.textUser(text)
        return(True)
    except:
        print('Cound not text user at this current time, Possible Disconnect from server...')
        return(False)
#returns true if the current time matches the parameters set in the config file
def eTimeCheck():
    global config
    ctime =[int(HM) for HM in time.strftime('%H,%M').split(',')]
    return((ctime[0]%2==config['Hour']) and (ctime[1]==config['Minute']) )
#trys to poll the subreddit, if it can't, text the user that it cant with the first 50 characters of the error
def tryPollAll():
    global masterLock
    global keywords
    global passes
    global polls
    global pingsT
    #try to poll the subreddit
    print('Trying to poll /r/'+config['Subreddit']+'...')
    try:
        pollAndPlace.pollAll()
        polls+=1
        print('Completed a Poll of /r/'+config['Subreddit']+'...')
        #problem child vvvvvvvv
        tryTextUser('Completed a Poll of /r/'+config['Subreddit']+'\nTotal Polls : '+str(polls))
        return(True)
    except Exception as e:
        tryTextUser('Could not poll /r/'+config['Subreddit']+'.\n\n'+str(e)[:50])
        print('Could not poll /r/'+config['Subreddit']+', possible disconnect from server...')
        return(False)
#run the program and have it check again every 60 seconds
def runnit():
    global masterLock
    global keywords
    global passes
    global polls
    global pingsT
    tryTextUser('Starting Up')
    print('Starting up...')
    try:
        while masterLock:
            print('Pass '+str(passes)+' of this Round')
            passes+=1
            print('Running Minute check...')
            bigBreak=False
            #if suspended, don't poll the subreddit
            if(not suspend):
                #if it is a certain time of day, do a poll and place
                print('Checking Time...')
                print(str(time.strftime('%H:%M:%S')))
                if eTimeCheck():
                    tryPollAll()
            #try to process emails and set the new keywords list. if there were no keywords,
            #it will be set to empty again
            print('Trying to process emails...')
            try:
                keywords=textUpdates.processEmails()
            except Exception as e:
                print('Email Processing failed to execute, Possible disconnect from server...')
                tryTextUser('Email Processing failed to execute, Possible disconnect from server.\n\n'+str(e)[:50])
            print('Trying to execute keywords...')
            for key in keywords:
                if key == 'suspend':
                    print('**')
                    print('keyword "suspend" found')
                    print('**')
                    flop()
                    if(suspend):
                        print('Reddit Polling Suspended...')
                        if(tryTextUser('Reddit Polling Suspended.')):
                            print('Successfully Notified User...')
                    else:
                        print('Reddit Polling Enabled...')
                        if(tryTextUser('Reddit Polling Enabled.')):
                            print('Successfully Notified User...')
                if key == 'masterlock-stop':
                    print('**')
                    print('keyword "masterlock-stop" found')
                    print('**')
                    masterLock=False
                if key == 'ping':
                    print('**')
                    print('keyword "ping" found')
                    print('**')
                    pingsT+=1
                    print('Pinging user back~~\nSystem is still online\nTotal Passes :'+str(passes)+'\nTotal Polls : '+str(polls)+'\nTotal Pings :'+str(pingsT))
                    if(tryTextUser('System is still online\nTotal Passes :'+str(passes)+'\nTotal Polls : '+str(polls)+'\nTotal Pings :'+str(pingsT))):
                        print('Successfully Pinged back User...')
                if key == 'force-poll':
                    print('**')
                    print('keyword "force-poll" found')
                    print('**')
                    tryPollAll()
                if key == 'restart':
                    print('**')
                    print('keyword "restart" found')
                    print('**')
                    print('-----RESTARTING-----')
                    keywords =['bigRestart']
                    bigBreak = True
                    break
            if bigBreak:
                break
            #wait 60 secods between anything
            print('Trying to sleep...')
            print('_______________________________________')
            try:
                time.sleep(60)
            except Exception as e:
                tryTextUser('the time module is not functioning properly\n\n'+str(e)[:50])
                break

        
        
    except Exception as e:
        tryTextUser('Something HORRIBLY WRONG has happened, program has ended.\n\n'+str(e)[:50])
while 'bigRestart' in keywords:
    runnit()
    tryTextUser('Shutting Down')
    print('Shutting Down...')
