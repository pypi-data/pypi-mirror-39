import argparse
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__file__)

def configure_action(args):
    print("configure")

def serve_action(args):

    class NaokoEventHandler(FileSystemEventHandler):
        
        def on_any_event(self, e):
            logger.info("event event event {}".format(e))

        def on_created(self, e):
            logger.info("")


    
    path = '/home/zkrhm/'
    event_handler = NaokoEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    parser = argparse.ArgumentParser()

    sparser = parser.add_subparsers()

    cfg_cmd = sparser.add_parser('configure')
    cfg_cmd.set_defaults(func=configure_action)
    svc_cmd = sparser.add_parser('serve')
    svc_cmd.set_defaults(func=serve_action)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()