import requests

from db import db
from tag_consts import MATH

PROBLEMS_REQUEST = "https://codeforces.com/api/problemset.problems?tags="

problems_set = requests.get(f"{PROBLEMS_REQUEST}{MATH}")

# TODO: ужасный преужасный костыль. Нужен чтобы упростить структуру бд, но мне нужно будет сделать поиск контеста по части сроки (% вроде бы)... 
def createId(id, index):
    return f"{id}{index}"

# для записи в таблицу нужно к id контеста добавлять код индекса задачи.
# print(createId(345, "A"))

for problem in problems_set.json()["result"]["problems"]:
    id = str(problem.get("contestId"))+problem.get("index")
    index = problem.get("index")
    name = problem.get("name")
    type = problem.get("type")
    points = problem.get("points")
    rating = problem.get("rating")
    tags = problem.get("tags")
    # print(problem)
    # try:
    db.addProblem(id, index, name, type, points, rating, tags)
    # except:
    #     pass

for statistic in problems_set.json()["result"]["problemStatistics"]:
    contestId = str(statistic["contestId"])
    index = statistic["index"]
    solvedCount = statistic["solvedCount"]

    db.addStatisticToProblem(contestId+index, solvedCount)
    # print(statistic)  

# db.printAll()
db.testDB()