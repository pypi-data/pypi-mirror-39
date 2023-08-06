# enduhub_downloader
Python package to download, clean and prepapare data from enduhuber.com.

```
from enduhub_downloader.runner import Runner as Runner

from enduhub_downloader.downloader import Downloader as Downloader

runner = Runner("First name", "Last_year", 1980) # first_name, last_name
# or
runner = Runner() 
runner.birth_year = 1980
runner.full_name = "FirstName LastName"

downloader = Downloader(runner, '2016-11-12') # this date is optional, it is the date to which the results are retrieved.
downloader.download_results()

print(runner)

runner.event_type_info() # Return agregate info about races counter, sum_distance
runner.event_best_time() # Return dictionery with best time with given event type and distance
```
