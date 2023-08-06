import multiprocessing
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import requests
import sseclient

CONNECTION_RETRY_INTERVAL_SEC = 3


class NotificationListener:
    def __init__(self, listen_url, app_key):
        self.listen_url = listen_url
        self.app_key = app_key
        self.process = None
        self.queue = None
        self.handlers = defaultdict(list)

    def on(self, event_name, handler):
        self.handlers[event_name].append(handler)

    def start(self):
        sse_url = self.listen_url + ('/' if not self.listen_url.endswith('/') else '') + self.app_key
        self.queue = multiprocessing.Queue()

        # A separate process is used to terminate it and close long-polling connection explicitly
        # (for some reasons a try to close the connection hangs if a thread is used)
        self.process = multiprocessing.Process(target=self.run, args=(sse_url, self.queue))
        self.process.start()

        executor = ThreadPoolExecutor(1)
        executor.submit(self.process_queue, self.queue)

    def run(self, sse_url, queue):
        while True:
            try:
                with requests.get(sse_url, stream=True, headers={'Accept': 'text/event-stream'}) as response:
                    client = sseclient.SSEClient(response.iter_content())
                    for event in client.events():
                        queue.put(event)
            except Exception:
                sleep(CONNECTION_RETRY_INTERVAL_SEC)

    def process_queue(self, queue):
        while True:
            event = queue.get()
            if event is None:
                break

            for handler in self.handlers[event.event]:
                handler(event)

    def stop(self):
        self.process.terminate()
        self.queue.put(None)
        self.queue.close()
        self.queue.join_thread()
