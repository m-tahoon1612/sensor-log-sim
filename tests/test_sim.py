import csv, os, tempfile, unittest
from sensorsim.bus import Bus, match
from sensorsim.sim import Sensor, CsvLogger, Alert, run
class T(unittest.TestCase):
    def test_match(self):
        self.assertTrue(match("home/+/temp", "home/kitchen/temp"))
        self.assertTrue(match("home/#", "home/a/b/c"))
        self.assertFalse(match("home/+/temp", "home/kitchen/hum"))
        self.assertFalse(match("home/+", "home/a/b"))
    def test_run_logs_and_alerts(self):
        bus = Bus(); d = tempfile.mkdtemp(); p = os.path.join(d, "log.csv")
        log = CsvLogger(p); alert = Alert(21.0)
        bus.subscribe("home/#", log); bus.subscribe("home/+/temp", alert)
        ss = [Sensor("kitchen","temp",21.0,0.5,seed=1), Sensor("bath","hum",55,2,seed=2)]
        run(bus, ss, 20, log); log.close()
        rows = list(csv.reader(open(p)))
        self.assertEqual(len(rows), 41)
        self.assertTrue(all(t == "home/kitchen/temp" for t,_ in alert.fired))
    def test_deterministic(self):
        a = Sensor("x","t",1,1,seed=3); b = Sensor("x","t",1,1,seed=3)
        self.assertEqual([a.read() for _ in range(5)], [b.read() for _ in range(5)])
if __name__ == "__main__": unittest.main()
