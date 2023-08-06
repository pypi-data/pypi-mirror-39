from enduhub_downloader.runner import Runner as Runner
from enduhub_downloader.downloader import Downloader as Downloader
runner = Runner(first_name="Świerc", last_name="Marcin", birth_year=1985)
downloader = Downloader(runner, '2016-11-12')
downloader.download_results()
print(runner.event_best_time('Bieganie', 10))
print(runner)
print(runner.event_type_info('Bieganie'))
print(runner.event_type_info('Bieganie'))


print(runner.event_type_info('Biegi Górskie'))
print(runner.event_type_info('Biegi Górskie'))
