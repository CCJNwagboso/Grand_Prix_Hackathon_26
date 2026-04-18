import json
from DataClasses.dataClasses import car, track, tyres, weather, race, tyre_set, race_config


def load_race_config(filepath: str) -> race_config:
    with open(filepath, "r") as f:
        data = json.load(f)

    c = data["car"]
    loaded_car = car(
        max_speed             = c["max_speed_m/s"],
        accel                 = c["accel_m/se2"],
        brake                 = c["brake_m/se2"],
        limp_constant         = c["limp_constant_m/s"],
        crawl_constant        = c["crawl_constant_m/s"],
        fuel_tank_capacity    = c["fuel_tank_capacity_l"],
        initial_fuel          = c["initial_fuel_l"],
        fuel_consumption_rate = c["fuel_consumption_l/m"],
        current_fuel          = c["initial_fuel_l"],
    )

    r = data["race"]
    loaded_race = race(
        name                          = r["name"],
        laps                          = r["laps"],
        base_pit_stop_time_s          = r["base_pit_stop_time_s"],
        pit_tyre_swap_time_s          = r["pit_tyre_swap_time_s"],
        pit_refuel_rate               = r["pit_refuel_rate_l/s"],
        corner_crash_penalty_s        = r["corner_crash_penalty_s"],
        pit_exit_speed                = r["pit_exit_speed_m/s"],
        fuel_soft_cap_limit           = r["fuel_soft_cap_limit_l"],
        starting_weather_condition_id = r["starting_weather_condition_id"],
        time_reference_s              = r["time_reference_s"],
    )

    loaded_track = [
        track(
            id       = seg["id"],
            type     = seg["type"],
            length_m = seg["length_m"],
            radius_m = seg.get("radius_m"),
        )
        for seg in data["track"]["segments"]
    ]

    tyre_properties = {
        compound: tyres(
            type                           = compound,
            life_span                      = props["life_span"],
            dry_friction_multiplier        = props["dry_friction_multiplier"],
            cold_friction_multiplier       = props["cold_friction_multiplier"],
            light_rain_friction_multiplier = props["light_rain_friction_multiplier"],
            heavy_rain_friction_multiplier = props["heavy_rain_friction_multiplier"],
            dry_degradation                = props["dry_degradation"],
            cold_degradation               = props["cold_degradation"],
            light_rain_degradation         = props["light_rain_degradation"],
            heavy_rain_degradation         = props["heavy_rain_degradation"],
            current_tyre_degradation       = 0.0,
        )
        for compound, props in data["tyres"]["properties"].items()
    }

    loaded_tyre_sets = [
        tyre_set(set_id=set_id, compound=entry["compound"], tyres=tyre_properties[entry["compound"]])
        for entry in data["available_sets"]
        for set_id in entry["ids"]
    ]

    loaded_weather = [
        weather(
            condition               = w["condition"],
            duration_s              = w["duration_s"],
            acceleration_multiplier = w["acceleration_multiplier"],
            deceleration_multiplier = w["deceleration_multiplier"],
        )
        for w in data["weather"]["conditions"]
    ]

    return race_config(
        car                  = loaded_car,
        race                 = loaded_race,
        track_segments       = loaded_track,
        tyre_sets            = loaded_tyre_sets,
        weather_schedule     = loaded_weather,
        starting_tyre_set_id = data["available_sets"][0]["ids"][0],
    )