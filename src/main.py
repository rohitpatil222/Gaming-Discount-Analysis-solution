from pathlib import Path
from step1_transform import transform_game_events
from step2_discount import apply_discounts

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

def main():
    events_df = transform_game_events(
        f"{DATA_DIR}/Input_Game_Events.json",
        f"{OUTPUT_DIR}/Output_Game_Events_Discounts.txt"
    )

    apply_discounts(
        f"{DATA_DIR}/Input_Start_Student_Discounts.txt",
        events_df,
        f"{OUTPUT_DIR}/Output_End_Students_Discounts.txt"
    )

if __name__ == "__main__":
    main()