class Problem:
    def __init__(self, problem_id: str, problem_index, name, type_, points, rating, statistic=-1):
        self.problem_id = problem_id
        self.problem_index = problem_index
        self.name = name
        self.type = type_
        self.points = points
        self.rating = rating
        self.statistic = statistic

    def __str__(self):
        return f"""
        **description**:
        
        Problem ID: {self.problem_id},
        Name: {self.name},
        Type: {self.type},
        Points: {self.points},
        Rating: {self.rating}
        
        (link)[https://codeforces.com/problemset/problem/{self.get_number_of_id()}/{self.problem_index}]
        """

    def get_number_of_id(self) -> str:
        nums = []
        for i in self.problem_id:
            if i.isalnum():
                nums.append(i)

        return "".join(nums)

    @classmethod
    def from_db_row(cls, row):
        """
        Создает экземпляр класса Problem из строки результата запроса к базе данных.
        """
        return cls(
            problem_id=row[0],
            problem_index=row[1],
            name=row[2],
            type_=row[3],
            points=row[4],
            rating=row[5],
            statistic=row[6]
        )
