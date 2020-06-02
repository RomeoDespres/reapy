import os

import httpwatcher
import tornado.ioloop


if __name__ == '__main__':
    server = httpwatcher.HttpWatcherServer(
        "build/html",
        watch_paths=["source"],
        on_reload=lambda: os.system(".\make.bat html"),
        host="127.0.0.1",
        port=5556,
        server_base_path="/",
        watcher_interval=1.0,
        recursive=True,
        open_browser=True
    )
    server.listen()
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        server.shutdown()
