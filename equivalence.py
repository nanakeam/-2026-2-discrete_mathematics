# 반사성: A 집합 내에 a에 대해 (a, a)
# 대칭성: A 집합 내에 (a, b)에 대해 (b, a)
# 추이성: A 집합 내에 (a, b)가 있고 (b, c)가 있으면 (a, c)
# 동치류: A 집합 내에 a와 순서쌍을 이루는 원소 집합
# 동치관계: 집합에 대한 관계가 반사관계, 대칭관계, 추이관계를 모두 만족

# 폐포: 순서쌍들을 추가해서 특정 성질을 만족시키는 것 


A = [1, 2, 3, 4, 5]
N = len(A)


# 관계 행렬 입력
def input_matrix():
    print("집합 A = {1, 2, 3, 4, 5}")
    print("5x5 관계 행렬을 입력하세요.")

    matrix = []

    for i in range(N):
        while True:
            values = input(f"{i+1}행: ").split()

            if len(values) == 5 and all(
                v in ("0", "1") for v in values
            ):
                matrix.append(list(map(int, values)))
                break # 입력 받은 데이터 리스트로 저장

            print("0 또는 1의 원소를 5개 입력하세요.")

    return matrix


# 반사성 판별
def is_reflexive(matrix):
    for i in range(N):
        if matrix[i][i] != 1: # [i][i]가 1일 때 반사성 만족
            return False
    return True

# 추가기능: 반사성 위반 위치 
def reflexive_violations(matrix):
    return [(A[i], A[i]) for i in range(N) if matrix[i][i] == 0]


# 대칭성 판별
def is_symmetric(matrix):
    for i in range(N):
        for j in range(N):
            if matrix[i][j] != matrix[j][i]: #[i][j] == [j][i]일 때 대칭성 만족
                return False
    return True

def symmetric_violations(matrix):
    return [
        ((A[i], A[j]), (A[j], A[i]))
        for i in range(N)
        for j in range(N)
        if matrix[i][j] == 1 and matrix[j][i] == 0
    ]

# 추이성 판별
def is_transitive(matrix):
    for i in range(N):
        for j in range(N):
            for k in range(N): # 원소 세 개 비교 
                if matrix[i][j] == 1 and matrix[j][k] == 1:
                    if matrix[i][k] != 1:
                        return False
    return True

def transitive_violations(matrix):
    return [
        ((A[i], A[j]), (A[j], A[k]), (A[i], A[k]))
        for i in range(N)
        for j in range(N)
        for k in range(N)
        if matrix[i][j] == 1 and matrix[j][k] == 1 and matrix[i][k] == 0
    ]


# 동치 관계 판별
def is_equivalence(matrix): 
    return (
        is_reflexive(matrix)
        and is_symmetric(matrix)
        and is_transitive(matrix) 
    )


# 동치류 출력
def equivalence_classes(matrix):
    for i in range(N):
        members = []

        for j in range(N):
            if matrix[i][j] == 1:
                members.append(A[j]) 

        print(f"[{A[i]}] = {set(members)}")


# 반사 폐포
def reflexive_closure(matrix):
    result = [row[:] for row in matrix]

    for i in range(N):
        result[i][i] = 1

    return result


# 대칭 폐포
def symmetric_closure(matrix):
    result = [row[:] for row in matrix]

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1 or matrix[j][i] == 1:
                result[i][j] = 1
                result[j][i] = 1

    return result


# 추이 폐포 (와샬 알고리즘)
def transitive_closure(matrix):
    result = [row[:] for row in matrix]

    for k in range(N):
        for i in range(N):
            for j in range(N):
                if result[i][k] == 1 and result[k][j] == 1:
                    result[i][j] = 1

    return result


# 최종 동치 폐포
def show_final_equivalence_closure(matrix):
    print("\n= 최종 동치 폐포 (반사 → 대칭 → 추이) =")
    result = [row[:] for row in matrix]

    steps = [
        ("반사", is_reflexive, reflexive_closure),
        ("대칭", is_symmetric, symmetric_closure),
        ("추이", is_transitive, transitive_closure),
    ]

    for name, check_function, closure_function in steps:
        print(f"\n[{name} 폐포 단계]")

        if check_function(result):
            print(f"{name}성을 만족하므로 변환하지 않습니다.")
        else:
            print("변환 전 행렬:")
            for row in result:
                print(row)

            result = closure_function(result)

            print("변환 후 행렬:")
            for row in result:
                print(row)

    print("\n최종 동치 폐포 행렬:")
    for row in result:
        print(row)

    print("\n최종 동치 관계 판별:")
    check_relation(result, show_violations=False)

    if is_equivalence(result):
        print("\n최종 동치류:")
        equivalence_classes(result)

# 세 폐포 순서대로 적용해서 동치 폐포 생성 
def equivalence_closure(matrix):
    result = reflexive_closure(matrix)
    result = symmetric_closure(result)
    result = transitive_closure(result)
    return result

# 동치 관계 판별 결과 출력
def check_relation(matrix, show_violations=True):
    r = is_reflexive(matrix)
    s = is_symmetric(matrix)
    t = is_transitive(matrix)

    print("반사성:", "만족" if r else "불만족")
    print("대칭성:", "만족" if s else "불만족")
    print("추이성:", "만족" if t else "불만족")
    print("동치 관계:", "맞음" if r and s and t else "아님")

    if show_violations:
        if not r:
            print("\n[반사성 위반] 빠진 순서쌍:")
            for pair in reflexive_violations(matrix):
                print(f"  {pair}")

        if not s:
            print("\n[대칭성 위반] 있는 순서쌍 → 빠진 순서쌍:")
            for existing, missing in symmetric_violations(matrix):
                print(f"  {existing} → {missing}")

        if not t:
            print("\n[추이성 위반] 있는 두 순서쌍 → 빠진 순서쌍:")
            for first, second, missing in transitive_violations(matrix):
                print(f"  {first}, {second} → {missing}")

    return r, s, t


# 각 폐포 결과를 판별하고 동치류 확인
def show_closure(name, matrix, closure_function):
    result = closure_function(matrix)

    print(f"\n= {name} 폐포 =")

    print("\n변환 전 행렬:")
    for row in matrix:
        print(row)

    print("\n변환 후 행렬:")
    for row in result:
        print(row)

    print("\n변환 후 동치 관계 재판별:")
    check_relation(result, show_violations=False)

    if is_equivalence(result):
        print("\n변환 후 동치류:")
        equivalence_classes(result)
    else:
        print("\n동치 관계가 아니므로 동치류를 출력할 수 없습니다.")


def main():
    matrix = input_matrix()
    print("\n= 입력 행렬 =")
    for row in matrix:
        print(row)
    print("\n= 최초 관계 판별 =")
    r, s, t = check_relation(matrix)
    if r and s and t:
        print("\n원래 관계의 동치류:")
        equivalence_classes(matrix)
    # 반사 폐포
    if r:
        print("\n= 반사 폐포 =")
        print("반사성을 만족하므로 변환하지 않습니다.")
    else:
        show_closure("반사", matrix, reflexive_closure)
    # 대칭 폐포
    if s:
        print("\n= 대칭 폐포 =")
        print("대칭성을 만족하므로 변환하지 않습니다.")
    else:
        show_closure("대칭", matrix, symmetric_closure)
    # 추이 폐포
    if t:
        print("\n= 추이 폐포 =")
        print("추이성을 만족하므로 변환하지 않습니다.")
    else:
        show_closure("추이", matrix, transitive_closure)
    show_final_equivalence_closure(matrix)
if __name__ == "__main__":
    main()
