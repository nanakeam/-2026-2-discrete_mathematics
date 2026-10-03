# 행렬 입력 받기 
def input_matrix():
    n = int(input("정방행렬의 차수를 입력하세요: "))

    matrix = []
    for i in range(n):
        while True:
            row = input(str(i + 1) + "행: ").split()
            if len(row) != n:
                print(n, "개의 숫자를 입력해주세요.")
                continue
            try:
                row = [float(x) for x in row]
                break
            except ValueError:
                print("숫자만 입력해주세요.")
        matrix.append(row)

    return matrix


# 2. 행렬식을 이용한 역행렬 계산
def get_minor(matrix, row, col):
    minor = [] # 소행렬 
    for i in range(len(matrix)):
        if i == row:
            continue
        new_row = []
        for j in range(len(matrix)):
            if j != col:
                new_row.append(matrix[i][j])
        minor.append(new_row)
    return minor


def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    # 여인수 전개
    det = 0
    for j in range(n):
        sign = (-1) ** j
        det += sign * matrix[0][j] * determinant(get_minor(matrix, 0, j))
    return det


def inverse_by_determinant(matrix):
    n = len(matrix)
    det = determinant(matrix)

    if abs(det) < 1e-10:
        print("오류: 행렬식이 0이므로 역행렬이 존재하지 않습니다.")
        return None

    if n == 1:
        return [[1 / det]]

    # 여인수 행렬 구하기
    cofactor = []
    for i in range(n):
        row = []
        for j in range(n):
            sign = (-1) ** (i + j)
            row.append(sign * determinant(get_minor(matrix, i, j)))
        cofactor.append(row)

    inverse = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(cofactor[j][i] / det)
        inverse.append(row)

    return inverse


# 3. 가우스-조던 소거법을 이용한 역행렬 계산
def inverse_by_gauss_jordan(matrix):
    n = len(matrix)

    # 첨가행렬
    aug = []
    for i in range(n):
        row = matrix[i][:]         
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        aug.append(row)

    for i in range(n):
        if abs(aug[i][i]) < 1e-10:
            swapped = False
            for k in range(i + 1, n):
                if abs(aug[k][i]) > 1e-10:
                    aug[i], aug[k] = aug[k], aug[i]
                    swapped = True
                    break
            if not swapped:
                print("오류: 역행렬이 존재하지 않습니다.")
                return None

        pivot = aug[i][i]
        for j in range(2 * n):
            aug[i][j] = aug[i][j] / pivot

        for k in range(n):
            if k != i:
                factor = aug[k][i]
                for j in range(2 * n):
                    aug[k][j] = aug[k][j] - factor * aug[i][j]

    inverse = []
    for i in range(n):
        inverse.append(aug[i][n:])
    return inverse


# 4. 결과 출력 및 비교 
def print_matrix(matrix):
    for row in matrix:
        for x in row:
            if abs(x) < 1e-10:     
                x = 0.0
            if abs(x - round(x)) < 1e-10:  
                print("%10.0f" % round(x), end="")
            else:
                print("%10.4f" % x, end="")
        print()


def is_same(a, b):
    for i in range(len(a)):
        for j in range(len(a)):
            if abs(a[i][j] - b[i][j]) > 1e-9:
                return False
    return True


# 5. 추가 기능: 역행렬 만든 걸 다시 역으로 만들어서 원본 행렬이 나오는지 검증
def check_inverse(A, inv):
    inv_inv = inverse_by_gauss_jordan(inv)
    if inv_inv is None:
        return False
    print_matrix(inv_inv)
    return is_same(A, inv_inv)


def main():
    A = input_matrix()

    print("\n행렬식으로 구한 역행렬:")
    inv1 = inverse_by_determinant(A)
    if inv1 is not None:
        print_matrix(inv1)

    print("\n가우스-조던 소거법으로 구한 역행렬:")
    inv2 = inverse_by_gauss_jordan(A)
    if inv2 is not None:
        print_matrix(inv2)

    print()
    if inv1 is None or inv2 is None:
        print("역행렬이 존재하지 않아 비교할 수 없습니다.")
        return

    if is_same(inv1, inv2):
        print("두 방법의 결과가 동일합니다.")
    else:
        print("두 방법의 결과가 다릅니다.")

    print("\n[추가 기능] (A⁻¹)⁻¹ 계산 결과:")
    if check_inverse(A, inv1):
        print("원래 행렬 A와 같으므로 올바른 역행렬입니다.")
    else:
        print("원래 행렬 A와 같지 않으므로 올바른 역행렬이 아닙니다.")


main()