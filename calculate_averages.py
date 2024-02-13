from random import choices
from json import load

NUM_SIMS = 100_000


def open_data(data: str) -> any:
    with open(data, "r", encoding="utf-8") as f:
        return load(f)


def simulate_bonk_pots(level_list: any, number_of_simulations: int = NUM_SIMS) -> list:
    POSSIBLE_BONKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    level_up_list = []
    for level in level_list:
        level_up_list.append(
            choices(POSSIBLE_BONKS, weights=level["probs"], k=number_of_simulations))
    return level_up_list


def calculate_average_exp(bonk_list: list, exp_dictionary: dict, number_of_simulations: int = NUM_SIMS):
    avg_exp_list = []
    for level_num, bonks in enumerate(bonk_list, start=141):
        avg_lvl_exp = 0
        for bonk in bonks:
            for i in range(bonk):
                avg_lvl_exp += exp_dictionary[str(level_num)]
        avg_lvl_exp /= number_of_simulations
        avg_exp_list.append(avg_lvl_exp)
    return avg_exp_list


def gen_final_list(avg_exp_list: list, bonk_list: list) -> list:
    avg_bonks = list(enumerate(zip(avg_exp_list, bonk_list), start=141))
    avg_bonks.sort(reverse=True, key=lambda x: x[1][0])
    return avg_bonks


def main() -> None:
    level_list = open_data(data="values.json")
    level_up_list = simulate_bonk_pots(level_list=level_list)
    EXP_DICT = {str(level["number"]): level["exp"] for level in level_list}
    average_exp_list = calculate_average_exp(
        bonk_list=level_up_list, exp_dictionary=EXP_DICT)
    for level, (exp, bonks) in gen_final_list(avg_exp_list=average_exp_list, bonk_list=level_up_list):
        print(f"|{level}|{
              exp}|{sum(bonks)/NUM_SIMS}|")


if __name__ == "__main__":
    main()
