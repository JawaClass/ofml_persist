import pandas as pd


def get_singleline_text(df: pd.DataFrame, language: str) -> str:
    result = df[df["language"] == language]
    return result["text"].iloc[0] if not result.empty else None


def get_multiline_text(df: pd.DataFrame, language: str) -> str:
    result = df[df["language"] == language]
    return "\n".join(result["text"]) if not result.empty else None


def get_language_2_text(df: pd.DataFrame, multi: bool) -> dict[str, str]:
    f = get_multiline_text if multi else get_singleline_text
    return {
        "de": f(df, "de"),
        "en": f(df, "en"),
        "fr": f(df, "fr"),
        "nl": f(df, "nl"),
    }
