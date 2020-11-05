import json

class Config:
    channel = None
    language = None
    segment_time = None
    engine = None
    engines = []
    targets = None

config = json.load(open('config.json'))

for p, value in config.items():
    setattr(Config, p, value)
