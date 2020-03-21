"""Fake Raspberry-Pi style sensors (temp/humidity) with a seeded random walk."""
import csv, random

class Sensor:
    def __init__(self, room, kind, start, step, seed=0):
        self.room, self.kind, self.value, self.step = room, kind, start, step
        self.rng = random.Random(seed)
    def read(self):
        self.value = round(self.value + self.rng.uniform(-self.step, self.step), 2)
        return self.value
    @property
    def topic(self):
        return "home/%s/%s" % (self.room, self.kind)

class CsvLogger:
    def __init__(self, path):
        self.f = open(path, "w", newline=""); self.w = csv.writer(self.f)
        self.w.writerow(["tick", "topic", "value"]); self.tick = 0
    def __call__(self, topic, value):
        self.w.writerow([self.tick, topic, value])
    def close(self):
        self.f.close()

class Alert:
    def __init__(self, limit):
        self.limit, self.fired = limit, []
    def __call__(self, topic, value):
        if value > self.limit:
            self.fired.append((topic, value))

def run(bus, sensors, ticks, logger=None):
    for t in range(ticks):
        if logger: logger.tick = t
        for s in sensors:
            bus.publish(s.topic, s.read())
