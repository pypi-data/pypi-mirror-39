from ..modules import  *


def LeakageModels(model='FowlerNordheim'):

    if model == 'SchottkyEmission':
        return lambda V, d, eps: 23.0543 * np.sqrt(V / (d * eps))  # d in units of nm
    elif model == 'SchottkyEmission2':
        return lambda V, d, eps: 23.0543 * np.sqrt(V / (d * eps))  # d in units of nm
    elif model == 'SimmonsSchottky':
        #        return lambda V, d, eps: 1 + 0.0072904*np.sqrt(V/(d*eps))
        return lambda V, d, eps: 1 + 23.0543 * np.sqrt(V / (d * eps))  # d in units of nm

    elif model == 'FowlerNordheim':
        # return lambda V, d, bar: 2+(6.83055e9*d*bar**1.5)/V
        return lambda V, d, bar: 2 + (6.83055 * d * bar ** 1.5) / V  # d in units of nm

    elif model == 'ThermionicEmission':
        return lambda V, d: 1 + 3.41446 * V ** 2 / d ** 2  # d in units of nm
    elif model == 'PooleFrenkel':
        return lambda V, d, eps: 1 + 46.1085 * np.sqrt(V / (d * eps))  #
    elif model == 'Hopping':
        return lambda V, d, a: 38.4173 * a * V / d  # both a and d in units of nm
    elif model == 'Ohmic':
        return lambda V: 1
    elif model == 'SpaceCharge':
        return lambda V: 2
    elif model == 'Offset':
        return lambda V, offs: offs * np.ones(len(V))