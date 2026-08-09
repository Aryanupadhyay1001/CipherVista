from queue import Queue


class PacketQueue:

    def __init__(self):

        self.queue = Queue()

    def put(self, packet):

        self.queue.put(packet)

    def get(self):

        if self.queue.empty():
            return None

        return self.queue.get()

    def empty(self):

        return self.queue.empty()