import sqlite3

from tag_consts import tagsId, idTags, IMPLEMENTATION, MATH

class ProblemsDataBase():


    def __init__(self) -> None:
        self.connect = sqlite3.connect('problems.db')
        self.cursor = self.connect.cursor()
        self.create_tables()

    def create_tables(self):
        cursor = self.cursor
        # структура задач
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Problems (
            problemId TEXT PRIMARY KEY, 
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
        self.connect.commit()

        # TODO: проверка что таблица существует 
        for pair in tagsId.items():
            cursor.execute("UPDATE Tags set tagName=? WHERE tagId=?", (pair[1], pair[0]))


    def get_problems_by_tag(self, tag_id):
        cursor = self.cursor
        cursor.execute("SELECT * FROM Problems p JOIN Problems_Tags pt ON p.problemId = pt.problemId WHERE pt.tagId =?", (tag_id,))
        rows = cursor.fetchall()
        return rows
    
    def get_one_problem_by_tag(self, tag_id):
        cursor = self.cursor
        cursor.execute("SELECT * FROM Problems p JOIN Problems_Tags pt ON p.problemId = pt.problemId WHERE pt.tagId =?", (tag_id,))
        row = cursor.fetchone()
        return row

    def get_problems_by_rating(self, rating: int):
        cursor = self.cursor
        cursor.execute("SELECT * FROM Problems WHERE rating=?", (rating,))
        rows = cursor.fetchall()
        return rows
    
    def get_problem_by_tag_rating(self, tag:str ,rating:int):
        cursor = self.cursor
        # Join Problems with Problems_Tags to get problems by tag
        cursor.execute("""
            SELECT p.* 
            FROM Problems p 
            JOIN Problems_Tags pt ON p.problemId = pt.problemId 
            WHERE pt.tagName =? AND p.rating =?
        """, (tag, rating))
        row = cursor.fetchone()
        return row


    def get_all_contest_problems(self, problem_id: str):
        cursor = self.cursor
        if problem_id[len(problem_id) - 1].isalnum():
            search_contest = F"{problem_id[0:len(problem_id)-2]}__"
        else:
            search_contest = F"{problem_id[0:len(problem_id)-1]}_"

        cursor.execute("SELECT * FROM Problems WHERE problemId LIKE?", (search_contest,))
        rows = cursor.fetchall()
        return rows

    def testDB(self):
        cursor = self.cursor
        self.create_tables()

        # cursor.execute("INSERT INTO Problems (problemId, problem_index, name, type, points, rating) VALUES ('69B', 'B', 'Bets', 'PROGRAMMING', 1000.0, 1200)")
        # cursor.execute("INSERT INTO ProIMPLEMENTATIONblems (problemId, problem_index, name, type, points, rating) VALUES ('55B', 'B', 'Bets', 'PROGRAMMING', 1000.0, 900)")
        # cursor.execute("INSERT INTO Problems (problemId, problem_index, name, type, points, rating) VALUES ('32A', 'A', 'Bets', 'PROGRAMMING', 1000.0, 800)")


        # for pair in tagsId.items():
        #     cursor.execute(f"INSERT INTO Tags (tagId, tagName) VALUES ({pair[0]}, '{pair[1]}' )")

        # cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({1}, {69})")
        # cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({1}, {55})")
        # cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({2}, {32})")

        # print(self.get_all_contest_problems("53C"))

        # self.addStatisticToProblem(69, 10000)
        print(self.get_one_problem_by_tag(idTags.get("bitmasks")))
        # print(self.get_problems_by_rating(2000))

        

    # TODO: обернуть в объект
    def addProblem(self, problemId, problem_index, name, problem_type, points, rating, tags: list):
        cursor = self.cursor

        cursor.execute(f"INSERT INTO Problems (problemId, problem_index, name, type, points, rating) VALUES ('{problemId}', '{problem_index}', '{name}', '{problem_type}', {points}, {rating})")
        for tag in tags:
            cursor.execute(F"INSERT INTO Problems_Tags (tagId, problemId) VALUES ({idTags.get(tag)}, {problemId})")

    
    def addStatisticToProblem(self, tag, solved_count):
        cursor = self.cursor
        cursor.execute("UPDATE Problems SET statistic =? WHERE problemId =?", (solved_count, tag))
        self.connect.commit()

    def printAll(self):
        cursor = self.cursor

        cursor.execute("SELECT * FROM Problems")
        print(cursor.fetchall())

        # TODO: напиши запросы по teg, problemId, points, rating

db = ProblemsDataBase()
# db.testDB()
