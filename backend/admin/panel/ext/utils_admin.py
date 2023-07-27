import math


def calculate_reading_time(text: str, char_per_second: int = 1200) -> int:
    characters = len(text)
    minutes = math.ceil(characters / char_per_second)
    return minutes