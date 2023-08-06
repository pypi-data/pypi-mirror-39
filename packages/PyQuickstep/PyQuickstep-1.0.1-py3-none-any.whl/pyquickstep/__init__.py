
from connections import  *



apilevel = "2.0"
threadsafety = 1 #Threads may share the module but not the connections
paramstyle = "pyformat"

def Connect(*args, **kwargs):

    #create connection and return
    return Connection(*args, **kwargs)

