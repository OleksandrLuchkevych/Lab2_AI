import random
from visualization import display_letter_as_matrix

def generate_matrix(rows, cols):
    numbers = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    matrix = []
    
    for _ in range(rows):
        row = [random.choice(numbers) for _ in range(cols)]
        matrix.append(row)
        
    return matrix

def get_random_array(x):
    if x == 'sa':
        return generate_matrix(17, 9)
    elif x == 'ar':
        return generate_matrix(1, 17)

matrix_sa = get_random_array('sa')
matrix_ar = get_random_array('ar')

weights_sa_x1 = []
weights_sa_x2 = []

def generate_weight_sa(X, weights):
    for row in matrix_sa:
        sum_weights = sum(X[i] * row[i] for i in range(len(X)))
        weights.append(round(sum_weights, 1))

X1 = [0.1, 0.2, 0.3]  
X2 = [0.4, 0.5, 0.6]  

generate_weight_sa(X1, weights_sa_x1)
generate_weight_sa(X2, weights_sa_x2)

def find_treshold_number(arr):
    numbers = list(map(float, arr))
    min_value = min(numbers)
    max_value = max(numbers)
    middle_value = (min_value + max_value) / 2
    
    closest = numbers[0]
    closest_diff = abs(middle_value - closest)

    for num in numbers:
        diff = abs(middle_value - num)
        if diff < closest_diff:
            closest_diff = diff
            closest = num
            
    return closest

def generate_weight_ar(result_sa):
    return round(sum(result_sa[i] * matrix_ar[0][i] for i in range(len(result_sa))), 1)

result_sa_x1 = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1]  
result_sa_x2 = [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0]  

weights_ar_x1 = generate_weight_ar(result_sa_x1)
weights_ar_x2 = generate_weight_ar(result_sa_x2)

def alpha_x(result_sa, weight, x1_or_x2):
    counter_alpha = 0
    sum_weights = weight
    count = 0
    array_alpha = []

    for i in range(17):
        if result_sa[i] == 1:
            array_alpha.append(matrix_ar[0][i])
            counter_alpha += 1
        else:
            array_alpha.append(0)
    
    if x1_or_x2 == 'x1':
        print('Для літери О: ')
        while sum_weights >= treshold_r:
            if sum_weights < treshold_r:
                break
            for i in range(len(array_alpha)):
                if array_alpha[i] > 0:
                    array_alpha[i] = round(array_alpha[i] - 0.1, 1)
                    sum_weights = round(sum_weights - 0.1, 1)
            count += 1
        print(f'Сума зміни ваг в альфа системі для літери О = {counter_alpha * 0.1}')
        display_letter_as_matrix('О')
    elif x1_or_x2 == 'x2':
        print('Для літери Л: ')
        while sum_weights < treshold_r:
            if sum_weights < treshold_r:
                break
            for i in range(len(array_alpha)):
                if array_alpha[i] < 1:
                    array_alpha[i] = round(array_alpha[i] + 0.1, 1)
                    sum_weights = round(sum_weights + 0.1, 1)
            count += 1
        print(f'Сума зміни ваг в альфа системі для літери Л = {counter_alpha * 0.1}')
        display_letter_as_matrix('Л')
    
    print(f'Тривалість навчання = {count}')
    print(f'Кінцева сума = {sum_weights}')
    print(f'Кінцевий масив ваг {array_alpha}')


treshold_r = 0.5  

alpha_x(result_sa_x1, weights_ar_x1, 'x1')
alpha_x(result_sa_x2, weights_ar_x2, 'x2')

def gamma_x(weights, result_sa_x1, result_sa_x2, n):
    N = len(weights)
    active_connections_s = sum(1 for x in result_sa_x1 if x == 1)
    passive_connections_s = sum(1 for x in result_sa_x1 if x == 0)
    active_connections_g = sum(1 for x in result_sa_x2 if x == 1)
    passive_connections_g = sum(1 for x in result_sa_x2 if x == 0)

    if active_connections_s == 0:
        print("Немає активних зв'язків для літери О.")
        return
    if active_connections_g == 0:
        print("Немає активних зв'язків для літери Л.")
        return

    cycle = 1
    iterations = 0
    sum_active = weights_ar_x1
    sum_passive = weights_ar_x2
    
    while sum_active > treshold_r or sum_passive < treshold_r:
        if cycle % 2 != 0:
            print(f'Ітерація {iterations + 1}: виконується перший цикл')
            correction_active = n - (active_connections_s * n) / N
            correction_passive = (-active_connections_s * n) / N
            for i in range(N):
                if result_sa_x1[i] == 1:
                    if weights[i] + correction_active >= 1:
                        correction_active = n - ((active_connections_s - 1) * n) / (N - 1)
                    weights[i] = max(0, min(1, weights[i] - correction_active))
                    sum_active -= correction_active
                else:
                    if weights[i] + correction_passive < 0:
                        correction_passive = (-((active_connections_s - 1) * n)) / (N - 1)
                    weights[i] = max(0, min(1, weights[i] - correction_passive))
                    sum_passive -= correction_passive
        else:
            print(f'Ітерація {iterations + 1}: виконується другий цикл')
            correction_active_v2 = n - (active_connections_g * n) / N
            correction_passive_v2 = (-active_connections_g * n) / N

            for i in range(N):
                if result_sa_x2[i] == 1:
                    if weights[i] + correction_active_v2 > 1:
                        correction_active_v2 = n - ((active_connections_g - 1) * n) / (N - 1)
                    weights[i] = max(0, min(1, weights[i] + correction_active_v2))
                    sum_passive += correction_active_v2
                else:
                    if weights[i] + correction_passive_v2 < 0:
                        correction_passive_v2 = (-((active_connections_g - 1) * n)) / (N - 1)
                    weights[i] = max(0, min(1, weights[i] + correction_passive_v2))
                    sum_active += correction_passive_v2
        cycle += 1
        iterations += 1

    sum_active_s = active_connections_s * 0.1 + (active_connections_s - (2 * active_connections_s ** 2) / N) * 0.1
    sum_active_g = active_connections_g * 0.1 + (active_connections_g - (2 * active_connections_g ** 2) / N) * 0.1
    print('Сума зміни ваг в гамма системі для літери О =', sum_active_s)
    print('Сума зміни ваг в гамма системі для літери Л =', sum_active_g)
    print('Кінцева сума звʼязків для літери О =', sum_active)
    print('Кінцева сума звʼязків для літери Л =', sum_passive)
    print('Оновлені ваги:', weights)

gamma_x(matrix_ar[0], result_sa_x1, result_sa_x2, 0.1)
