from typing import List, Tuple
import garth

# Mapping Logic
SPORT_TYPE_MAPPING = {
    "running": {"sportTypeId": 1, "sportTypeKey": "running", "displayOrder": 1},
    "cycling": {"sportTypeId": 2, "sportTypeKey": "cycling", "displayOrder": 2},
    "swimming": {"sportTypeId": 4, "sportTypeKey": "swimming", "displayOrder": 5},
    "strength": {"sportTypeId": 5, "sportTypeKey": "strength_training", "displayOrder": 9},
    "cardio": {"sportTypeId": 6, "sportTypeKey": "cardio_training", "displayOrder": 8},
}

STEP_TYPE_MAPPING = {
    "warmup": {"stepTypeId": 1, "stepTypeKey": "warmup", "displayOrder": 1},
    "cooldown": {"stepTypeId": 2, "stepTypeKey": "cooldown", "displayOrder": 2},
    "interval": {"stepTypeId": 3, "stepTypeKey": "interval", "displayOrder": 3},
    "recovery": {"stepTypeId": 4, "stepTypeKey": "recovery", "displayOrder": 4},
    "rest": {"stepTypeId": 5, "stepTypeKey": "rest", "displayOrder": 5},
    "repeat": {"stepTypeId": 6, "stepTypeKey": "repeat", "displayOrder": 6},
}

TARGET_TYPE_MAPPING = {
    "no target": {"workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target", "displayOrder": 1},
    "power": {"workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone", "displayOrder": 2},
    "cadence": {"workoutTargetTypeId": 3, "workoutTargetTypeKey": "cadence.zone", "displayOrder": 3},
    "heart rate": {"workoutTargetTypeId": 4, "workoutTargetTypeKey": "heart.rate.zone", "displayOrder": 4},
    "speed": {"workoutTargetTypeId": 5, "workoutTargetTypeKey": "speed.zone", "displayOrder": 5},
    "pace": {"workoutTargetTypeId": 6, "workoutTargetTypeKey": "pace.zone", "displayOrder": 6},
}

DISTANCE_UNIT_MAPPING = {
    "m": {"unitId": 2, "unitKey": "m", "factor": 1},
    "km": {"unitId": 3, "unitKey": "km", "factor": 1000},
    "mile": {"unitId": 4, "unitKey": "mile", "factor": 1609.344},
}

END_CONDITION_TYPE_MAPPING = {
    "time": {"conditionTypeId": 2, "conditionTypeKey": "time", "displayOrder": 2, "displayable": True},
    "distance": {"conditionTypeId": 3, "conditionTypeKey": "distance", "displayOrder": 3, "displayable": True},
    "lap.button": {"conditionTypeId": 1, "conditionTypeKey": "lap.button", "displayOrder": 1, "displayable": True},
    "iterations": {"conditionTypeId": 7, "conditionTypeKey": "iterations", "displayOrder": 7, "displayable": False},
}

DEFAULT_PACE = {
    "running": 0.36, "cycling": 0.05, "swimming": 0.5, "walking": 0.3, "strength": 0.36, "cardio": 0.36,
}

# The Client Class
class GarminClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.client = garth.Client()

    def login(self):
        try:
            self.client.login(self.email, self.password)
        except Exception as e:
            raise Exception(f"Garmin login failed: {str(e)}")

    def get_workouts(self, count=5):
        self.login()
        return self.client.connectapi("/workout-service/workout/list", params={"start": 0, "limit": count})

# Helper Functions
def get_sport_type(sport_type_key: str) -> dict:
    sport_type = SPORT_TYPE_MAPPING.get(sport_type_key.lower())
    if not sport_type:
        raise ValueError(f"Unsupported sport type: {sport_type_key}")
    return sport_type

def make_payload(workout: dict) -> dict:
    step_order = 1
    sport_type = get_sport_type(workout["type"])
    payload = {
        "sportType": sport_type,
        "workoutName": workout["name"],
        "workoutSegments": [{"segmentOrder": 1, "sportType": sport_type, "workoutSteps": []}],
    }
    return payload
