import pandas as pd

def apply_discounts(start_discount_path: str,
                    events_df: pd.DataFrame,
                    output_path: str) -> pd.DataFrame:
    """
    Step 2:
    Apply DS / DH differential discounting and
    write Output_End_Students_Discounts.txt
    """

    discounts = pd.read_csv(start_discount_path)

    for _, evt in events_df.iterrows():
        student_id = evt["StudentId"]
        minutes = evt["PlayMinutes"]
        event_type = evt["EventType"]

        if event_type == "DS":
            discounts.loc[
                (discounts.StudentId == student_id) &
                (discounts.PlaysetType == "S"),
                "DiscountMinutes"
            ] += minutes

            discounts.loc[
                (discounts.StudentId == student_id) &
                (discounts.PlaysetType == "H"),
                "DiscountMinutes"
            ] -= minutes
        else:  # DH
            discounts.loc[
                (discounts.StudentId == student_id) &
                (discounts.PlaysetType == "S"),
                "DiscountMinutes"
            ] -= minutes

            discounts.loc[
                (discounts.StudentId == student_id) &
                (discounts.PlaysetType == "H"),
                "DiscountMinutes"
            ] += minutes

    discounts.to_csv(output_path, index=False)

    agg = discounts.groupby("StudentId")["DiscountMinutes"].sum()

    print(f"Student with MIN discount minutes: {agg.idxmin()}")
    print(f"Student with MAX discount minutes: {agg.idxmax()}")

    return discounts
