from enduhub_downloader.race_result import RaceResult
from enduhub_downloader.best_result import BestResult

class EventTypeGroup:
  """
  A class used to represent an group info about event type

  Attributes
  ----------
  name :str
    name of event type
  couter :int
    holding information how many this type exist 
  sum_distance :float
    summary kilometeres of event_type
  best_result :dict
    info about best results

  """

  def __init__(self, name):
    """
    Parameters
    ----------
      name: str
      
    """

    self.name = name
    self.counter = 0
    self.sum_distance = 0.0
    self.best_results = []

  def __str__(self):
    return f'{self.name}, counter: {self.counter}, sum of the distances: {self.sum_distance}km' 
    
  def __add__(self, other):
    if type(other) == EventTypeGroup:
      if self.name != other.name:
        raise ValueError("You can't add event type group with different name")
      self.counter += other.counter  
      self.sum_distance += other.sum_distance
    elif type(other) == RaceResult:
      if self.name != other.race_type:
        raise ValueError("You can't race result to  event type group with different race_type")
      self.counter += 1
      self.sum_distance += other.distance
      self.calculate_best_result(other)
    
    return self


  def calculate_best_result(self, race_result):
    temp_best_result = BestResult(race_result.race_type, race_result.distance, race_result.time_result, race_result.result_date)
    temp_best_result.counter  = 1
    try:
      index = self.best_results.index(temp_best_result)
      best = self.best_results[index]
      if race_result.time_result < best.best_time:
        best.best_time = race_result.time_result
        best.counter += 1  
    except ValueError:
      self.best_results.append(temp_best_result)   

 




        
  