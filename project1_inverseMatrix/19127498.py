import math

def read_file(file_name_in):
    matrix = []
    with open(file_name_in) as f:
        for line in f:
            matrix.append(line.split())
    
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] = int(matrix[i][j])
    f.close()
    return matrix
      
def write_file(file_name_out, determinant, inverse_matrix):
    f = open(file_name_out, "w")

    f.write("Det: " + str(determinant))
    f.write("\n\n")

    f.write("Inverse matrix: \n")
    if inverse_matrix: 
        for i in range(len(inverse_matrix)):
            for j in range(len(inverse_matrix)):
                f.write(str(inverse_matrix[i][j]) + " ")
            f.write("\n")
    else: f.write("None")
    
    f.close()
    
    
# MY OTHER FUNCTIONS
def is_zero(x):
    # kiểm tra số thực x có là số thực 0 (rất gần 0)
    return math.isclose(x, 0, abs_tol = 1e-09)
    # |a - b| <= 0.00000000001 --> a ~ b

def is_zero_vector(v):
    return all(is_zero(vi) for vi in v)

def add_vector(v, w):
    return [vi + wi for vi, wi in zip(v, w)]

def sub_vector(v, w):
    return [vi - wi for vi, wi in zip(v, w)]

def mul_scalar_vector(alpha, v):
    return [alpha*vi for vi in v]

def equal_vector(v, w):
    return is_zero_vector(sub_vector(v, w)) # 2 vector bằng nhau khi hiệu của chúng là vector không

def row_switch(A, i, k):
    "di <-> dk"
    A[i], A[k] = A[k], A[i]
    
def row_mul(A, i, alpha):
    "di = anpha*di"
    A[i] = mul_scalar_vector(alpha, A[i])

def row_add(A, i, k, alpha):
    "di = di + anpha*dk"
    A[i] = add_vector(A[i], mul_scalar_vector(alpha, A[k]))
    
def Gauss_elimination(A, leading1 = True):
    R = A.copy()
    m, n = len(R), len(R[0]) # kích thước ma trận
    sign = 1
    row = col = 0
    
    while row < m:
        # Bước 1
        while col < n and all(is_zero(R[i][col]) for i in range(row, m)):
            col += 1
        if col == n:    # đã có dạng bậc thang
            break
        
        # Bước 2 (chọn dòng đầu tiên có số hạng khác 0)
        pivot_row = row + [not is_zero(R[i][col]) for i in range(row, m)].index(True)
        row_switch(R, row, pivot_row)
        if (pivot_row != row): sign = sign * -1

        # Bước 3 (tùy chọn leading 1)
        if leading1:
            row_mul(R, row, 1/R[row][col])
            sign = sign * 1/R[row][col]

        # Bước 4
        for i in range(row + 1, m):
            multiplier = R[i][col]/R[row][col]
            row_add(R, i, row, -multiplier) # di = di - drow * multiplier

        # Bước 5
        row += 1

    return R, sign

def calc_determinant_row_operation(matrix):
    echelon_matrix, sign =  Gauss_elimination(matrix, leading1 = False)
    det = sign

    for i in range (len(echelon_matrix)):
        det = det * echelon_matrix[i][i]
    return det

def invert_matrix_row_operation(matrix):
    res = []
    det = calc_determinant_row_operation (matrix)
    if det == 0:  return res

    temp = [[] for _ in matrix]
    for i, row in enumerate(matrix):
        assert len(row) == len(matrix)
        temp[i].extend(row + [0] * i + [1] + [0] * (len(matrix) - i - 1))
        
    R, sign = Gauss_elimination(temp, leading1 = True)

    for i in range(len(R)):
        for j in range(i + 1, int(len(R)), 1):
            multiplier = (R[i][j]) / (R[j][j])
            row_add(R, i, j, -multiplier)

    for i in range(len(R)):
        res.append(R[i][len(R[i])//2:])

    return res


# MY MAIN
def main():
    matrix = read_file(file_name_in = 'input.txt')
    
    det = calc_determinant_row_operation(matrix)
    inv_mat = invert_matrix_row_operation(matrix)
    
    write_file(file_name_out = '19127498_output.txt', determinant = det, inverse_matrix = inv_mat)

main()

