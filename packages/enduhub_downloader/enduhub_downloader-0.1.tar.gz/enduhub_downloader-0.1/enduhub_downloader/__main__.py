from enduhub_downloader.runner import Runner as Runner
from enduhub_downloader.downloader import Downloader as Downloader
runner = Runner("Michał", "Mojek", 1980)
downloader = Downloader(runner, '2016-11-12')
downloader.download_results()
print(runner)
