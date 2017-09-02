import factor_test as factor


def resolve_factor(line):
    line = line.replace(' ', '')
    l = line.split('=')
    factor_name = l[0]
    if len(l) == 1:
        base_factor_name = factor_name
        method = None
    else:
        l = l[1][:-1].split('(')
        method = [l[0]]
        l = l[1].split(',')
        base_factor_name = l[0]
        method += [l[1:]]
    return factor_name, base_factor_name, method


def resolve_condition(line):
    line = line.replace(' ', '')
    l = line.split('=')
    condition_name = l[0]
    l = l[1][:-1].split('(')
    method = [l[0]]
    l = l[1].split(',')
    method += [l]
    return condition_name, method


if __name__ == '__main__':
    input_factors = 'MA5 = MA(close,5)\nMA10 = MA(close, 10)'
    input_condition = 'gx = CROSS(MA5, MA10)'

    input_factors_lines = input_factors.split('\n')
    for line in input_factors_lines:
        if len(line) > 1:
            print resolve_factor(line)

    input_condition_lines = input_condition.split('\n')
    for line in input_condition_lines:
        if len(line) > 1:
            print resolve_condition(line)
