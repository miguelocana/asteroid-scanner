class MatrixService:

    def __init__(self, vectorized_matrix: str, n_cols: int):
        self.matrix = self.parse_vector(vectorized_matrix, n_cols)
        self.cols = len(self.matrix[0])
        self.rows = len(self.matrix)

    def _get_nearest_col_index(self, reverse: bool = False) -> int:
        range_func = range(len(self.matrix[0]) - 1, -1, -1) if reverse else range(len(self.matrix[0]))
        for col in range_func:
            if any(row[col] == 1 for row in self.matrix):
                return col
        return -1

    def _get_nearest_row_index(self, reverse: bool = False) -> int:
        range_func = range(len(self.matrix) - 1, -1, -1) if reverse else range(len(self.matrix))
        for row in range_func:
            if any(col == 1 for col in self.matrix[row]):
                return row
        return -1

    def _get_matrix_limit_indexes(self) -> tuple:
        left = self._get_nearest_col_index()
        right = self._get_nearest_col_index(reverse=True)
        top = self._get_nearest_row_index()
        bottom = self._get_nearest_row_index(reverse=True)
        return top, right, bottom, left

    def normalize(self) -> None:
        normalized_matrix = self.matrix
        top, right, bottom, left = self._get_matrix_limit_indexes()

        normalized_matrix = normalized_matrix[top:bottom + 1]
        normalized_matrix = [row[left:right + 1] for row in normalized_matrix]

        self.rows = len(normalized_matrix)
        self.cols = len(normalized_matrix[0])

        self.matrix = normalized_matrix
        self.vector = self.matrix_to_vector(normalized_matrix)

    @staticmethod
    def matrix_to_vector(matrix: list) -> str:
        return ''.join(str(num) for row in matrix for num in row)

    @staticmethod
    def parse_vector(vector: str, n_cols: int):
        res = []
        for i in range(0, len(vector), n_cols):
            arr = list(map(lambda n: int(n), vector[i: i + n_cols]))
            diff = n_cols - len(arr)
            if diff != 0:
                arr += [0] * diff
            res.append(arr)
        return res

    @property
    def as_array(self):
        return self.matrix

    @property
    def as_vector(self):
        return self.matrix_to_vector(self.matrix)
