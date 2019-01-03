#reads the config file and returns a dictionary with
#the contents of the config file
def readConfig():
    config ={}
    with open('config.txt','r') as cFile:
        for line in cFile:
            line = line.strip().split(':')
            try:
                config[line[0]] = int(line[1])
            except:
                config[line[0]] = str(line[1])
    return(config)
