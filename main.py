from DataClasses.dataClasses import race_config, tyres
from DataClasses.loader import load_race_config
from Methods.equations import *
from Actions.actions import *


class GrandPrixSimulator:
    def __init__(self, config: race_config):
        self.car              = config.car
        self.race             = config.race
        self.track_segments   = config.track_segments
        self.tyre_sets        = config.tyre_sets
        self.weather_schedule = config.weather_schedule
        self.current_tyre: tyres = next(
            ts.tyres for ts in config.tyre_sets
            if ts.set_id == config.starting_tyre_set_id
        )
        self.current_weather = config.weather_schedule[0]
        self.elapsed_time_s  = 0.0


if __name__ == "__main__":
    config = load_race_config("1.txt")
    sim = GrandPrixSimulator(config)