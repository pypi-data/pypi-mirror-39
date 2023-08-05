from luigi.interface import _WorkerSchedulerFactory

from .scheduler import CustomRemoteScheduler


class CustomSchedulerFactory(_WorkerSchedulerFactory):

    def create_remote_scheduler(self, url):
        return CustomRemoteScheduler(url)
