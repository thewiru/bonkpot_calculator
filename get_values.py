from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from json import dump


def gen_exp_list(driver: webdriver) -> list:

    exp_list = []
    driver.get("https://whackybeanz.com/calc/everything-exp#pills-exp-table")
    sleep(1)
    EXP_TABLE = driver.find_element(
        By.ID, "exp-table-4").find_elements(By.CSS_SELECTOR, "td")
    for row in EXP_TABLE:
        exp = row.get_attribute("data-raw-exp-tnl")
        if exp is not None:  # Note to reader: Use Pandas instead of doing something like this, I did this on a whim and I was lazy
            exp_list.append(int(exp))
    return exp_list


def gen_prob_list(driver: webdriver) -> list:
    prob_list = []
    driver.get("https://forum.gamer.com.tw/C.php?bsn=7650&snA=1026159&tnum=1")
    sleep(1)
    PROB_TABLE = driver.find_element(
        By.XPATH, "/html/body/div[5]/div/div[2]/section[1]/div[2]/div[2]/article/div/div[4]/table").find_elements(By.CSS_SELECTOR, "tr")[1:]
    for row in PROB_TABLE:
        tmp_list = []
        for cell in row.find_elements(By.CSS_SELECTOR, "td")[1:]:
            tmp_list.append(int(cell.text))
        prob_list.append(tuple(tmp_list))

    return prob_list


def grab_data() -> zip:
    options = Options()
    options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        exp_list = gen_exp_list(driver=driver)
        prob_list = gen_prob_list(driver=driver)
    return zip(exp_list, prob_list)


def save_data(data: zip) -> None:
    level_list = []

    for level_num, (level_exp, level_prob) in enumerate(data, start=141):
        level_list.append(
            {"number": level_num, "exp": level_exp, "probs": level_prob})

    with open("values.json", "w") as f:
        dump(level_list, f, ensure_ascii=False)


def main() -> None:
    data = grab_data()
    save_data(data=data)


if __name__ == "__main__":
    main()
