import sqlite3

from tag_consts import tagsId, idTags, IMPLEMENTATION, MATH

class ProblemsDataBase():


    def __init__(self) -> None:
        self.connect = sqlite3.connect('problems.db')
        self.cursor = self.connect.cursor()

    def create_tables(self):
        cursor = self.cursor
        # структура задач
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Problems (
            problemId INTEGER PRIMARY KEY,
            problem_index CHAR(1) NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            points REAL NOT NULL,
            rating INTEGER NOT NULL,
            statistic INTEGER DEFAULT -1
        )
        """)

        # наши теги
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tags (
        tagId INTEGER PRIMARY KEY,
        tagName TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Problems_Tags (
        tagId INTEGER NOT NULL,
        problemId INTEGER NOT NULL,
        FOREIGN KEY (tagId) REFERENCES Tags(tagId),
        FOREIGN KEY (problemId) REFERENCES Problems(problemId),
        PRIMARY KEY (tagId, problemId)
        )
        """)
        

    def get_problems_by_tag(self, tag_id):
        cursor = self.cursor
        cursor.execute("SELECT p.problemId, p.problem_index, p.name, p.type, p.points, p.rating, p.statistic FROM Problems p JOIN Problems_Tags pt ON p.problemId = pt.problemId WHERE pt.tagId =?", (tag_id,))
        rows = cursor.fetchall()
        return rows

    def testDB(self):
        cursor = self.cursor
        self.create_tables()

        cursor.execute("INSERT INTO Problems (problemId, problem_index, name, type, points, rating) VALUES (69, 'B', 'Bets', 'PROGRAMMING', 1000.0, 1200)")
        cursor.execute("INSERT INTO Problems (problemId, problem_index, name, type, points, rating) VALUES (55, 'B', 'Bets', 'PROGRAMMING', 1000.0, 900)")
        cursor.execute("INSERT INTO Problems (problemId, problem_index, name, type, points, rating) VALUES (32, 'A', 'Bets', 'PROGRAMMING', 1000.0, 800)")


        for pair in tagsId.items():
            cursor.execute(f"INSERT INTO Tags (tagId, tagName) VALUES ({pair[0]}, '{pair[1]}' )")

        cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({1}, {69})")
        cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({1}, {55})")
        cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({2}, {32})")

        print(self.get_problems_by_tag(1))

        self.addStatisticToProblem(69, 10000)
        print(self.get_problems_by_tag(1))

        

    # TODO: обернуть в объект
    def addProblem(self, problemId, problem_index, name, problem_type, points, rating, tags: list):
        cursor = self.cursor

        cursor.execute(f"INSERT INTO Problems (problemId, problem_index, name, type, points, rating) VALUES ({problemId}, '{problem_index}', '{name}', '{problem_type}', {points}, {rating})")
        for tag in tags:
            cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({idTags.get(tag)}, {problemId})")

        
    
    def addStatisticToProblem(self, tag, solved_count):
        cursor = self.cursor
        cursor.execute("UPDATE Problems SET statistic =? WHERE problemId =?", (solved_count, tag))
        self.connect.commit()

