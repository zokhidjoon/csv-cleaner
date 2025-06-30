import pandas as pd

def clean_data(df, fill_missing=True, fill_value="N/A"):
    original_shape = df.shape

    # Replace empty strings or whitespace-only cells with proper NA
    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)

    # Drop completely empty rows
    df.dropna(how='all', inplace=True)

    # Drop columns that are mostly empty
    df.dropna(thresh=len(df) * 0.5, axis=1, inplace=True)

    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # Drop rows with any missing values if user doesn't want to fill
    if not fill_missing:
        df.dropna(inplace=True)

    # Fill missing values smartly
    if fill_missing:
        # Determine if user fill_value is numeric
        try:
            numeric_fill_value = float(fill_value)
            is_numeric_fill = True
        except ValueError:
            is_numeric_fill = False
            numeric_fill_value = 0  # default fallback for numeric columns

        for col in df.columns:
            if df[col].isna().sum() > 0:
                if df[col].dtype == 'object':
                    df[col].fillna(fill_value, inplace=True)
                else:
                    # Always use a number for numeric columns
                    df[col].fillna(numeric_fill_value, inplace=True)

    # Optional: Clean up money-like strings from object columns
    for col in df.select_dtypes(include='object').columns:
        try:
            df[col] = df[col].str.replace(r'[$,]', '', regex=True)
        except:
            pass  # skip non-string-compatible columns

    # Summary
    cleaned_shape = df.shape
    cleaning_summary = {
        "original_rows": original_shape[0],
        "original_cols": original_shape[1],
        "final_rows": cleaned_shape[0],
        "final_cols": cleaned_shape[1],
        "rows_removed": original_shape[0] - cleaned_shape[0],
        "cols_removed": original_shape[1] - cleaned_shape[1],
    }

    return df, cleaning_summary
