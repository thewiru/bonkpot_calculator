from os.path import exists
from json import load


def open_data(data: str) -> any:
    with open(data, "r", encoding="utf-8") as f:
        return load(f)


def calculate_avg_bonks(level_list: any) -> list:
    POSSIBLE_BONKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    avg_bonk_list = []
    for level in level_list:
        avg_bonks = 0
        for bonks, bonk_prob in zip(POSSIBLE_BONKS, level["probs"]):
            avg_bonks += bonks*bonk_prob/100
        avg_bonk_list.append(avg_bonks)
    return avg_bonk_list


def calculate_avg_exp(level_list: any) -> list:
    EXP_DICT = {str(level["number"]): level["exp"] for level in level_list}
    avg_exp_list = []
    for level in level_list:
        avg_level_exp = 0
        reduced_prob_list = list(filter(lambda x: x != 0, level["probs"]))
        for level_dif, prob in enumerate(reduced_prob_list):
            avg_level_exp += EXP_DICT[str(level["number"]+level_dif)]*prob/100
        avg_exp_list.append(avg_level_exp)
    return avg_exp_list


def gen_list(exp_list: list, bonk_list: list) -> list:
    final_list = list(enumerate(zip(exp_list, bonk_list), start=141))
    return final_list


def main() -> None:
    if not exists("values.json"):
        from get_values import grab_data, save_data
        data = grab_data
        save_data(data=data)
    level_list = open_data(data="values.json")
    avg_bonks = calculate_avg_bonks(level_list=level_list)
    avg_exp = calculate_avg_exp(level_list=level_list)
    for level, (exp, bonks) in gen_list(exp_list=avg_exp, bonk_list=avg_bonks):
        print(f"Level: {level} Avg Exp: {exp:.2f} Avg Bonks:{bonks:.2f}")


if __name__ == "__main__":
    main()
