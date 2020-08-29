# sensor-log-sim

Playing with the idea of a home sensor setup before buying a Pi: fake temp/humidity sensors publish onto an in-process MQTT-style bus (`+`/`#` wildcards), a CSV logger and a threshold alert subscribe. Stdlib only.

```
python -m unittest discover -s tests -t .
```
