import csv
import json

from logger import log_event
from Sheep import Sheep


def get_round_info(round_number: int,
                   wolf_x_pos: float,
                   wolf_y_pos: float,
                   sheep_list: list[Sheep],
                   rounds_list: list[dict]) -> list[dict]:
    sheep_pos = [(sheep.x_pos, sheep.y_pos) for sheep in sheep_list]

    new_round = {
        "round_no": round_number,
        "wolf_pos": (wolf_x_pos, wolf_y_pos),
        "sheep_pos": sheep_pos,
    }

    rounds_list.append(new_round)
    return rounds_list


def save_round_to_json(rounds_list: list[dict]) -> None:
    try:
        json_string = json.dumps(rounds_list)
        json_string = format_json_str(json_string, indent=4)
        with open('pos.json', 'w', encoding='utf-8') as file:
            file.write(json_string)
            log_event(10, "Saved to pos.json")
    except Exception as e:
        log_event(40, f'Unable to save to pos.json: {e}')


def format_json_str(string: str, indent: int) -> str:
    dict_indent = 1 * indent * " "
    key_indent = 2 * indent * " "
    end_sheep_list_indent = 3 * indent * " "
    sheep_list_indent = 4 * indent * " "
    replacements = {
        "]]}, {":
            f']\n{end_sheep_list_indent}]\n{dict_indent}'
            + "},\n" + f'{dict_indent}' + "{ ",
        "[{":
            f'[\n{dict_indent}' + "{ ",
        " \"":
            f'\n{key_indent}\"',
        "[[":
            f'[\n{sheep_list_indent}[',
        "], [":
            f'],\n{sheep_list_indent}[',
        "]}]":
            f'\n{end_sheep_list_indent}]\n{dict_indent}' + "}" + "\n]"
    }
    for key, value in replacements.items():
        string = string.replace(key, value)
    return string


def save_round_to_csv(alive_list: list[tuple]) -> None:
    try:
        with open('alive.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Round", "Alive number"])
            writer.writerows(alive_list)
            log_event(10, "Saved to alive.csv")
    except Exception as e:
        log_event(40, f'Unable to save to alive.csv: {e}')
