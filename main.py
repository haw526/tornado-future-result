from tornado.web import Application
from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.netutil import bind_sockets
from tornado.httpserver import HTTPServer
from tornado.process import fork_processes
from concurrent.futures import ThreadPoolExecutor
import os

class Handler(RequestHandler):
    def initialize(self, pool):
        self.executor = pool

    def get(self, *args, **kwargs):
        future = self.future_result_test()
        IOLoop.current().add_future(future=future, callback=self.future_result_callback)

    @run_on_executor
    def future_result_test(self):
        print 'future return result, sleep 5s'
        import time
        time.sleep(5)
        return {'a': 1}

    def future_result_callback(self, future):
        print 'future result callback....'
        print future.result()


def main():
    pool = ThreadPoolExecutor(max_workers=16)
    app = Application([
        ('/', Handler, dict(pool=pool)),

    ],
    template_path=os.path.join(os.path.dirname(__file__), 'template'),
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    )
    sockets = bind_sockets(1888)
    fork_processes(1)
    server = HTTPServer(app)
    server.add_sockets(sockets)
    IOLoop.current().start()


if __name__ == '__main__':
    main()