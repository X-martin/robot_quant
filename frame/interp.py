import factor_filter as fnf


def interp_factor(line):
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


def interp_filter(line, factor_dict_keys):
    factor_list = []
    method = []

    line = line.replace(' ', '')
    l = line.split('=')
    filter_name = l[0]
    l = l[1][:-1].split('(')
    method += [l[0]]
    l = l[1].split(',')
    for a in l:
        if a in factor_dict_keys:
            factor_list += [a]
            l.remove(a)
    method += [l]
    return filter_name, factor_list, method


def interp(factor_txt, filter_txt):
    factor_dict = {}
    filter_dict = {}
    factor_lines = factor_txt.split('\n')
    filter_lines = filter_txt.split('\n')
    for line in factor_lines:
        if len(line)>1:
            factor_name, base_factor_name, method = interp_factor(line)
            f = fnf.FactorT(base_factor_name, method)
            factor_dict[factor_name] = f
    for line in filter_lines:
        if len(line)>1:
            filter_name, factor_list, method = interp_filter(line, factor_dict.keys())
            f = fnf.FilterT(factor_list, method)
            filter_dict[filter_name] = f
    return factor_dict, filter_dict

if __name__ == '__main__':
    factor_txt = 'MA5 = MA(close,5)\nMA10 = MA(close, 10)'
    filter_txt = 'gx = CROSS(MA5, MA10)'

    d1, d2 = interp(factor_txt, filter_txt)
    print d1
    print d2
