# enduhub_downloader 0.2
Python package to download, clean and prepapare data from enduhuber.com.

```
from enduhub_downloader.runner import Runner as Runner

from enduhub_downloader.downloader import Downloader as Downloader

runner = Runner(first_name="First name", last_name="Last_year", birth_year=1980) # first_name, last_name
# or
runner = Runner(full_name = "FirstName LastName", birth_year = 1980)

downloader = Downloader(runner, '2016-11-12') # this date is optional, it is the date to which the results are retrieved.
downloader.download_results()

print(runner)

# event_type_info return agregate info about races counter, sum_distance
runner.event_type_info('Bieganie')['counter']
runner.event_type_info('Bieganie')['sum_distance']

# event_best_time return dictionery with best time with given event type and distance
runner.event_best_time('Bieganie', 10)
runner.event_best_time('Bieganie', 42.1) #marathon
```
## 0.21 The release notes
- change init runner
- event_type_info update when dont find run type, return dict with zeros {counter: 0, sum_distance: 0}

## 0.2 The release notes
- Fix error with atypical distance

