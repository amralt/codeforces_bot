import requests

from tag_consts import IMPLEMENTATION

PROBLEMS_REQUEST = "https://codeforces.com/api/problemset.problems?tags="

problems_set = requests.get(f"{PROBLEMS_REQUEST}{IMPLEMENTATION}")

# для записи в таблицу нужно к id контеста добавлять код индекса задачи.

print(problems_set.content)
# for problem in problems_set.content:
#     print(problem) 