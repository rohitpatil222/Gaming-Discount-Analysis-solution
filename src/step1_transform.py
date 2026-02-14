import json
import pandas as pd
from datetime import datetime

def _to_datetime(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")

def transform_game_events(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Step 1:
    Parse JSON game events and write Output_Game_Events_Discounts.txt
    """

    rows = []

    with open(input_path, "r") as f:
        payload = json.load(f)

    for event in payload.get("events", []):
        play_minutes = 0.0
        responses = 0
        successes = 0

        for rnd in event.get("data", []):
            start = _to_datetime(rnd["roundStartTime"])
            end = _to_datetime(rnd["roundEndTime"])

            play_minutes += (end - start).total_seconds() / 60

            target = rnd.get("targetText", [None])[0]
            resp = rnd.get("responseText", [])

            responses += len(resp)
            successes += sum(1 for r in resp if r == target)

        rows.append({
            "EventId": event["eventId"],
            "StudentId": event["studentId"],
            "EventType": "DH" if event["playsetType"] == "H" else "DS",
            "PlayMinutes": round(play_minutes, 2),
            "NoOfResponses": responses,
            "NoOfSuccessfulResponses": successes
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return df
