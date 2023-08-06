import re
from datetime import timedelta
from datetime import datetime


class RaceResult:
    """
    A class used to represent a race result

    ....

    Attributes
    ----------
    name :str
        name of the race
    result_date :date
        date of the event
    distance :int 
        distance of the event in km  
    race_type :str
        race type 
    time_result :timedelta
        reult of the race    
    
    Methods
    -------
    

    """
    def __init__(self, name, result_date, distance, race_type, time_result):
        """
        Parameters
        ----------
        name :str
            name of the race
        result_date :str
            date of the event
        distance: str
            distance of the event in km  
        race_type :str
            race type 
        time_result :str
            result of the race    
        """
        self.name = name
        self.result_date = result_date
        self.distance = distance
        self.race_type = race_type
        self.time_result = time_result
        #self.distance = self.dict_distance()
    
   
    def __str__(self):
        return f'{self.name}: {self.distance} km, {self.time_result}, {self.result_date}'
    
    def __repr__(self):
       return f"RaceResult('{self.name}', '{self.result_date}'', '{self.distance} km', '{self.race_type}', '{self.time_result}')"
    
    

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, new_name):
        """Clean name"""
        new_name = re.sub(' +',' ', new_name)
        self._name = new_name.replace('\n','')

    @property
    def distance(self):
        return self._distance
        
    @distance.setter
    def distance(self, dist):
        """Translate run name to distance"""
        result = False
        run_size = dist
        if run_size == 'Maraton':
            result =  42.1
        elif run_size == 'Półmaraton':
            result = 21.05
        elif 'km' in run_size:
            result = float(run_size[:-3].replace(',','.'))
        else:
            result =  None
       
        self._distance = result

   
    @property
    def time_result(self):
        return self._time_result

    @time_result.setter
    def time_result(self, string_time):
        """Parse string and change  to time delta"""
        ti = string_time.split(':')
        try:
            hour = int(ti[0])
            minute = int(ti[1])
            second = int(ti[2])
        except ValueError:
            #logger.error("Wrong time format. Skipped result")
            time_delta =  None
        except IndexError:
            #logger.error("Wrong time format. Skipped result")
            time_delta =  None    
        else:
            time_delta =  timedelta(hours=hour, minutes=minute, seconds=second)
        self._time_result = time_delta        

    @property
    def result_date(self):
        return self._result_date

    @result_date.setter
    def result_date(self, string_date):
        """Parse string and change to date"""
        string_date = datetime.strptime(string_date, '%Y-%m-%d')
        self._result_date = string_date.date()    
    
        

   