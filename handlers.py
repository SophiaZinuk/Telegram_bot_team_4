import telebot
'''
#decorator of time limit

import time

def rate_limiter(max_call:int=3, limit_sec:int=60):
    times_call=[]
    def decor(func):
        def wrapper(*args, **kwargs):
            times_call.append(time.time())
            # difference between first  and last attempts
            diff_sec=times_call[-1]-times_call[0] 
            # if diff more than limit, start again
            if diff_sec>limit_sec:
                del times_call[-2::-1]
                diff_sec=0
            # check amount of attempts in limit period
            if len(times_call)>max_call and diff_sec<=limit_sec:                
                return f'Time is not over. Try again later'            
            return func(*args, **kwargs) 
        return wrapper
    return decor

@rate_limiter(max_call=3, limit_sec=60)
def func(num:int, txt:str='txt')->int:
    return num

'''
class Request():
    def __init__(self, id_user, status=0):
        self.id_user=id_user
        self.id_request
        self.adress
        self.telephone
        self.target
        self.message=''
        self.date
        self.status=status

    def add_id_request(self, id_request):
        self.id_request=id_request

    def add_adress(self, adress):
        self.adress=adress

    def add_telephone(self, telephone):
        self.telephone=telephone
    
    def add_target(self, target):
        self.target=target
    
    def add_message(self, message):
        self.message=message
    
    def add_date(self, date):
        self.date=date

    def add_status(self, status):
        self.date=status

'''
'id_request': google_sheets.get_id_rqst(), #number of previos id+1
           'id_user': user_avto.from_user.id, 
           'adress': google_sheets.get_adress(user_avto.from_user.id), 
           'telephone': google_sheets.get_telephone(user_avto.from_user.id),
           'target':rqst[0],
           'num_avto': rqst[1], 
           'message': rqst[2], #??
           'date': user_avto.date,
           'status': 0
'''