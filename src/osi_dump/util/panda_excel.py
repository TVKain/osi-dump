import pandas as pd

from pandas import DataFrame


def expand_list_column(df: DataFrame, column: str) -> DataFrame:
    # Find the maximum length of the list in the column
    max_len = df[column].apply(len).max()

    # Create a DataFrame from the list column
    expanded_df = pd.DataFrame(
        df[column].apply(lambda x: x + [None] * (max_len - len(x))).tolist(),
        index=df.index,
    )

    # Rename the columns
    expanded_df.columns = [f"{column}_{i+1}" for i in range(expanded_df.shape[1])]

    # Drop the original column and join the expanded columns
    df = df.drop(column, axis=1).join(expanded_df)

    return df
