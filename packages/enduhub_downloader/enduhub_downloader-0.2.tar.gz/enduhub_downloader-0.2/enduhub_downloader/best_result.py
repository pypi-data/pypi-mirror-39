
class BestResult:
  """
  A class used to represent an group info about event type

  Attributes
  ----------
  event_type_name :str
    event type name
  distance :str
    distance in km
  best_time : timedelta
    best time on distance


  """

  def __init__(self, event_type_name, distance, best_time, result_date):
    """
    Parameters
    ----------
      event_type_name: str
      
    """

    self.event_type_name = event_type_name
    self.distance = distance
    self.best_time = best_time
    self.result_date = result_date
    self.counter = 0
    

  def __str__(self):
    return f'{self.event_type_name}, distance: {self.distance},counter:{self.counter}, best time : {self.best_time}, result date: {self.result_date}' 

  def __eq__(self, other):
    return self.event_type_name == other.event_type_name and self.distance == other.distance 

    



  