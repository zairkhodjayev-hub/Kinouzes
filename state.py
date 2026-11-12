from aiogram.dispatcher.filters.state import State,StatesGroup


class addchannelr(StatesGroup):
    name = State()    
    username = State()    
    channelid = State()

class addchannel(StatesGroup):
    name = State()    
    username = State()    
    channelid = State()

class detelechannel(StatesGroup):
    channelid = State()        

class addmoviestate(StatesGroup):
    Video = State()          
    VideoCaption = State()    
    Trailer = State()         
    TrailerVideo = State()    
 

class detelemovie(StatesGroup):
    moviecode = State()    

class reklama(StatesGroup):
    videoandcaption = State()     
    description = State()          