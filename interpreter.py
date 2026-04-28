from typing import Optional


# 0 =  ┘    └
#        ██  
#      ┐    ┌

# 1 =  ┴────┴ ou ──────
#        ██        ██
#      ┐    ┌    ┐    ┌

# 2 = ┘    ├ ou ┘    │
#       ██ │      ██ │
#     ┐    ├    ┐    │

# 3 = ┴────┼ ou ─────┐
#       ██ │      ██ │
#     ┐    ├    ┐    │   

# 4 = ┘    └ ou ┘    └
#       ██        ██
#     ┬────┬    ──────

# 5 = ┴────┴ ou ──────
#       ██        ██
#     ┬────┬    ──────

# 6 = ┘    ├ ou ┘    │
#       ██ │      ██ │
#     ┬────┼    ─────┘

# 7 = ┴────┼ ou ─────┐
#       ██ │      ██ │
#     ┬────┼    ─────┘

# 8 = ┤    └ ou │    └
#     │ ██      │ ██  
#     ┤    ┌    │    ┌

# 9 = ┼────┴ ou ┌─────
#     │ ██      │ ██ 
#     ┤    ┌    │    ┌

# 10/A = ┤    ├ ou │    │
#        │ ██ │    │ ██ │
#        ┤    ├    │    │

# 11/B = ┼────┼ ou ┌────┐
#        │ ██ │    │ ██ │
#        ┤    ├    │    │

# 12/C = ┤    └ ou │    └
#        │ ██      │ ██ 
#        ┼────┬    └─────

# 13/D = ┼────┴ ou ┌─────
#        │ ██      │ ██ 
#        ┼────┬    └─────

# 14/E = ┤    ├ ou │    │
#        │ ██ │    │ ██ │
#        ┼────┼    └────┘

# 15/F = ┼────┼ ou ┌────┐
#        │ ██ │    │ ██ │
#        ┼────┼    └────┘


def interpreter(
        maze : list[list],
        start: int, exit: int,
        color_num : int,
        solution: list[int]
        ):
    count = 0
    spe_color  = "\033[0m"
    color_list = ["\033[0;37m", "\033[0;31m", "\033[0;32m", "\033[0;34m"]
    base_color = "\033[0m"
    for i in maze:
        for j in i:
            if (j in "04"):
                print(f"{color_list[color_num]}┘    └{base_color}", end="")
            if (j in "15"):
                print(f"{color_list[color_num]}──────{base_color}", end="")
            if (j in "26"):
                print(f"{color_list[color_num]}┘    │{base_color}", end="")
            if (j in "37"):
                print(f"{color_list[color_num]}─────┐{base_color}", end="")
            if (j in "8C"):
                print(f"{color_list[color_num]}│    └{base_color}", end="")
            if (j in "9D"):
                print(f"{color_list[color_num]}┌─────{base_color}", end="")
            if (j in "AE"):
                print(f"{color_list[color_num]}│    │{base_color}", end="")
            if (j in "BF"):
                print(f"{color_list[color_num]}┌────┐{base_color}", end="")
        print("")
        for j in i:
            count += 1
            if (count == start):
                spe_color = "\033[0;34m"
            elif (count == exit):
                spe_color = "\033[0;31m"
            elif (count in solution):
                spe_color = "\033[38;5;205m"
            else:
                spe_color = "\033[0m"
            if (j in "0145"):
                print(f"  {spe_color}██{base_color}  ", end="")
            if (j in "2367"):
                print(f"  {spe_color}██ {color_list[color_num]}│{base_color}", end="")
            if (j in "89CD"):
                print(f"{color_list[color_num]}│ {spe_color}██{base_color}  ", end="")
            if (j in "ABEF"):
                print(f"{color_list[color_num]}│ {spe_color}██ {color_list[color_num]}│{base_color}", end="")
        print("")
        for j in i:
            if (j in "01"):
                print(f"{color_list[color_num]}┐    ┌{base_color}", end="")
            if (j in "23"):
                print(f"{color_list[color_num]}┐    │{base_color}", end="")
            if (j in "45"):
                print(f"{color_list[color_num]}──────{base_color}", end="")
            if (j in "67"):
                print(f"{color_list[color_num]}─────┘{base_color}", end="")
            if (j in "89"):
                print(f"{color_list[color_num]}│    ┌{base_color}", end="")
            if (j in "AB"):
                print(f"{color_list[color_num]}│    │{base_color}", end="")
            if (j in "CD"):
                print(f"{color_list[color_num]}└─────{base_color}", end="")
            if (j in "EF"):
                print(f"{color_list[color_num]}└────┘{base_color}", end="")
        print("")
