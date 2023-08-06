import re
from enduhub_downloader.event_type_group import EventTypeGroup

class Runner:
    """
    A class used to represent an runner

    ....

    Attributes
    ----------
    first_name :str
        first name of the runner
    last_name :str
        last name of the runner    
    birth_year :int
        birth year of runner
    short_birth_year :int
        two digit representations of birth year
    race_results :list
        list of race results  
    event_counter :dict
        hold information about event types couts, bests_times

    Methods
    -------
    full_name        
    """
    def __init__(self, first_name='', last_name='', birth_year=None):
        """
        Parameters
        ----------
        first_name: str
            First name of the runner
        last_name : str
            Last name of the runner
        birth_year : int, optional
            Birth year of the runner
        """
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.race_results = []
        self.event_counter = {}
        self.event_type_groups = []
        
    def __str__(self):
        info = '{} {}, {}'.format(self.first_name, self.last_name, self.birth_year)
        info +='\n'
        info +="Event counter:\n"
        for eg in self.event_type_groups:
            info += f" - {str(eg)}"
            info +='\n'
            for br in eg.best_results:
                info += f" -- {str(br)}"
                info +='\n'
        info +='\n'    
        return info
        
    @property
    def full_name(self):
        """Return Merge first name and last name."""
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def short_birth_year(self):
        """Return two digits represetation of birth year."""
        cutted_year=str(self.birth_year)[-2:]  
        return  int(cutted_year)

    @full_name.setter
    def full_name(self, name):
        name = re.sub(' +',' ', name)
        self._full_name = name
        split_full_name = name.split(' ')
        self.first_name = split_full_name[0]
        self.last_name = split_full_name[1]

    def add_race_result(self, race_result):
        """Add race result to the runner"""
        if race_result.time_result and race_result.distance: 
            self.race_results.append(race_result)    
            self.event_type_counter(race_result)
    
    def event_type_groups_exist(self, race_result):
        for x in self.event_type_groups:
            if x.name == race_result.race_type:
                return x
        return None

    def event_type_counter(self, race_result):
        """Add run to even counter atribute and return event_counter"""
        event_type_group = self.event_type_groups_exist(race_result)
        if not event_type_group:
            event_type_group = EventTypeGroup(race_result.race_type)
            self.event_type_groups.append(event_type_group)
        return event_type_group + race_result

    def event_type_info(self,name_event_type):
        for etg in self.event_type_groups:
            if name_event_type == etg.name:
                return {'counter': etg.counter, 'sum_distance': etg.sum_distance}

    def event_best_time(self, name_event_type, distance):
        """Return dictionery with best time with given event type and distance """
        for etg in self.event_type_groups:
            if name_event_type == etg.name:
               for br in etg.best_results:
                    print(etg.name, br.distance, distance,  br.best_time)
                    if br.distance == distance:
                        return br.best_time

