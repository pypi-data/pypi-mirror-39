"""This module holding data about Runner"""

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

    def __init__(self, **kwargs):
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
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.birth_year = kwargs.get('birth_year')
        if 'full_name' in kwargs:
            self.full_name = kwargs.get('full_name')
        self.race_results = []
        self.event_counter = {}
        self.event_type_groups = []

    def __str__(self):
        info = '{} {}, {}'.format(
            self.first_name, self.last_name, self.birth_year)
        info += '\n'
        info += "Event counter:\n"
        for eg_type in self.event_type_groups:
            info += f" - {str(eg_type)}"
            info += '\n'
            for best_result in eg_type.best_results:
                info += f" -- {str(best_result)}"
                info += '\n'
        info += '\n'
        return info

    @property
    def full_name(self):
        """Return Merge first name and last name."""
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def short_birth_year(self):
        """Return two digits represetation of birth year."""
        cutted_year = str(self.birth_year)[-2:]
        return int(cutted_year)

    @full_name.setter
    def full_name(self, name):
        name = re.sub(' +', ' ', name)
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
        """Check if event group exist for given race_result"""
        for event_type_group in self.event_type_groups:
            if event_type_group.name == race_result.race_type:
                return event_type_group
        return None

    def event_type_counter(self, race_result):
        """Add run to even counter atribute and return event_counter"""
        event_type_group = self.event_type_groups_exist(race_result)
        if not event_type_group:
            event_type_group = EventTypeGroup(race_result.race_type)
            self.event_type_groups.append(event_type_group)
        return event_type_group + race_result

    def event_type_info(self, name_event_type):
        """Find eventy type by given name"""
        for event_type_group in self.event_type_groups:
            if name_event_type == event_type_group.name:
                return {'counter': event_type_group.counter,
                        'sum_distance': event_type_group.sum_distance}
            return {'counter': 0, 'sum_distance': 0}

    def event_best_time(self, name_event_type, distance):
        """Return dictionery with best time with given event type and distance """
        for event_type_group in self.event_type_groups:
            if name_event_type == event_type_group.name:
                for best_result in event_type_group.best_results:
                    print(event_type_group.name, best_result.distance,
                          distance, best_result.best_time)
                    if best_result.distance == distance:
                        return best_result.best_time
        return None
