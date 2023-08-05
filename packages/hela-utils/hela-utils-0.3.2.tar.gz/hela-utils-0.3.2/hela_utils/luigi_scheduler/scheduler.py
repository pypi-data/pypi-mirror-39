from requests import Session
from luigi.rpc import RemoteScheduler

from .requests_fetcher import CustomRequestsFetcher



class CustomRemoteScheduler(RemoteScheduler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fetcher = CustomRequestsFetcher(Session())
