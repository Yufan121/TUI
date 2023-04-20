import threading
import time

class ThreadManager:
    def __init__(self):
        self.threads = {}
        self.paused = set()
        self.stop_event = threading.Event()

    def add_thread(self, name, target, args=()):
        thread = threading.Thread(target=self._run, args=(target, args), name=name)
        self.threads[thread.ident] = thread
        return thread.ident

    def _run(self, target, args):
        while not self.stop_event.is_set():
            if threading.current_thread().ident in self.paused:
                time.sleep(0.1)
                continue
            target(*args)

    def start_all(self):
        for thread in self.threads.values():
            thread.start()

    def join_all(self):
        for thread in self.threads.values():
            thread.join()

    def terminate(self, name_or_id):
        if isinstance(name_or_id, str):
            for thread in self.threads.values():
                if thread.name == name_or_id:
                    self.threads.pop(thread.ident)
                    break
        else:
            self.threads.pop(name_or_id)

    def pause(self, name_or_id):
        if isinstance(name_or_id, str):
            for thread in self.threads.values():
                if thread.name == name_or_id:
                    self.paused.add(thread.ident)
                    break
        else:
            self.paused.add(name_or_id)

    def restart(self, name_or_id):
        if isinstance(name_or_id, str):
            for thread in self.threads.values():
                if thread.name == name_or_id:
                    self.paused.discard(thread.ident)
                    break
        else:
            self.paused.discard(name_or_id)

def task1():
    print("Task 1 started")
    # do something
    print("Task 1 finished")

def task2():
    print("Task 2 started")
    # do something
    print("Task 2 finished")

manager = ThreadManager()
id1 = manager.add_thread("task1", task1)
id2 = manager.add_thread("task2", task2)
manager.start_all()
time.sleep(1)
manager.pause(id1)
time.sleep(1)
manager.restart(id1)
time.sleep(1)
manager.terminate(id2)
manager.join_all()
