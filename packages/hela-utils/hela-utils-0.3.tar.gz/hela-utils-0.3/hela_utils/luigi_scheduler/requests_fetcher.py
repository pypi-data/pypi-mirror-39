from luigi.rpc import RequestsFetcher



class CustomRequestsFetcher(RequestsFetcher):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session.trust_env = False

    def check_pid(self):
        super().check_pid()
        self.session.trust_env = False

