"""Запуск из корня проекта: python -m stage1_lev"""

import argparse

from . import exercise01, exercise02, exercise03, exercise04, exercise06, exercise06a
from .reporting import display, export


def main():
    parser = argparse.ArgumentParser(description="Решения заданий по SimPy")
    parser.add_argument("--exercise", choices=("all", "1", "2", "3", "4", "6", "6a"), default="all")
    parser.add_argument("--seed", type=int, default=42, help="Seed случайных потоков")
    parser.add_argument("--log", action="store_true", help="Показать все события")
    parser.add_argument("--output", help="Каталог выгрузки CSV и JSON")
    parser.add_argument("--compare", action="store_true", help="Парные запуски задания 6: выход открыт/закрыт до 60 с")
    parser.add_argument("--demo", action="store_true", help="Сценарий методички для 4, 6 или 6a")
    parser.add_argument("--spillback", action="store_true", help="Девять автомобилей и запрет проезда C до 180 с в 6a")
    args = parser.parse_args()
    if args.compare:
        if args.exercise != "6" or args.demo or args.spillback:
            parser.error("--compare используется отдельно с --exercise 6")
        for scenario, result in zip(("open", "blocked"), exercise06.compare(args.seed)):
            print(f"Scenario: {scenario}")
            display(result, args.log)
            if args.output:
                print(f"Saved: {export(result, args.output, scenario=scenario)}")
        return
    if args.spillback and (args.exercise != "6a" or args.demo):
        parser.error("--spillback используется отдельно с --exercise 6a")
    if args.demo and args.exercise not in ("4", "6", "6a"):
        parser.error("--demo требует --exercise 4, 6 или 6a")
    runners = {"1": exercise01.run, "2": exercise02.run,
               "3": lambda: exercise03.run(args.seed),
               "4": lambda: exercise04.run(args.seed),
               "6": lambda: exercise06.run(args.seed),
               "6a": lambda: exercise06a.run(args.seed)}
    if args.demo:
        runners[args.exercise] = {"4": exercise04.demo, "6": exercise06.demo,
                                  "6a": exercise06a.demo}[args.exercise]
    if args.spillback:
        runners["6a"] = exercise06a.spillback_demo
    selected = runners if args.exercise == "all" else (args.exercise,)
    for number in selected:
        result = runners[number]()
        display(result, show_log=args.log or number in ("1", "2"))
        if args.output:
            print(f"Saved: {export(result, args.output)}")


if __name__ == "__main__":
    main()
