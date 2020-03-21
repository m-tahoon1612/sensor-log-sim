"""Tiny in-process MQTT-ish pub/sub with + and # wildcards."""
from collections import defaultdict

def match(pattern, topic):
    p, t = pattern.split("/"), topic.split("/")
    for i, part in enumerate(p):
        if part == "#":
            return True
        if i >= len(t) or (part != "+" and part != t[i]):
            return False
    return len(p) == len(t)

class Bus:
    def __init__(self):
        self.subs = defaultdict(list)
    def subscribe(self, pattern, fn):
        self.subs[pattern].append(fn)
    def publish(self, topic, payload):
        n = 0
        for pat, fns in self.subs.items():
            if match(pat, topic):
                for fn in fns:
                    fn(topic, payload); n += 1
        return n
