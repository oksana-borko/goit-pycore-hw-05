
import sys
from collections import Counter

LOG_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> dict:

    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"Invalid log line: {line.strip()!r}")

    date, time, level, message = parts
    if level not in LOG_LEVELS:
        raise ValueError(f"Unknown log level {level!r} in line: {line.strip()!r}")

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> list:

    logs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                print(f"Warning (line {line_number}): {error}", file=sys.stderr)
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:

    return list(filter(lambda log: log["level"] == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:

    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict) -> None:

    print(f"{'Рівень логування':<17}| Кількість")
    print(f"{'-' * 17}|{'-' * 10}")
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def display_log_details(logs: list, level: str) -> None:

    print(f"\nДеталі логів для рівня '{level.upper()}':")
    if not logs:
        print("Записів не знайдено.")
        return
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python task_3.py <path_to_log_file> [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None

    if level and level.upper() not in LOG_LEVELS:
        print(f"Unknown level '{level}'. Available: {', '.join(LOG_LEVELS)}")
        sys.exit(1)

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        sys.exit(1)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error reading file '{file_path}': {error}")
        sys.exit(1)

    if not logs:
        print("No valid log records found.")
        return

    display_log_counts(count_logs_by_level(logs))

    if level:
        display_log_details(filter_logs_by_level(logs, level), level)


if __name__ == "__main__":
    main()