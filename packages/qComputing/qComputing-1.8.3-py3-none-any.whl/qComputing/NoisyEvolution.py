from qComputing import Gates as g
from qComputing import Operations as op
import numpy as np
from decimal import *
import multiprocessing as mp
from lea import *
from multiprocessing import Pool
from functools import partial
import math

n_cpu = mp.cpu_count()  # We are getting the number of cores for any parallel method we shall need


def decohere(K, rho, n):
    """
    :param K: List of kraus operators
    :param rho: density matrix of system
    :param n: Number of qubits
    :return: Return evolved density matrix
    """
    parts = 8
    split_list = np.array_split(K, parts)

    with Pool(parts) as p:
        par_kraus = partial(serial_decohere, rho_s=rho, n_s=n)
        subout = p.map(par_kraus, split_list)
        out_map = serial_decohere(subout, rho, n)
        return out_map


def serial_decohere(K, rho_s, n_s):
    """
    :param K: List of kraus operators
    :param rho: density matrix of system
    :param n: Number of qubits
    :return: Return evolved density matrix
    """
    K = list(K)
    out = np.zeros((pow(2, n_s), pow(2, n_s)), dtype=complex)
    try:
        assert type(K) == list
        for i in range(len(K)):
            out += np.dot(K[i], np.dot(rho_s, op.ctranspose(K[i])))
    except:
        raise TypeError('The input K must be a list of numpy arrays')
    return out


def kraus_pta(n, t, t1, t2):
    """
    Produces the kraus matrices for the pta channel
    :param n: number of qubit
    :param t: time step for evolution
    :param t1: relaxation time
    :param t2: dephasing time
    :return: returns a 3 dimensinal array of pta kraus matrices
    """
    gamma = 1 - np.exp(-t / t1)
    t_phi = Decimal(1 / t2) - Decimal(1 / (2 * t1))
    # lambda1 = np.exp(-t/t1)*(1-np.exp(-2*(t/t_phi)))
    px = py = gamma / 4.0
    pz = 1.0 / 2.0 - py - np.exp(-t / (2 * t1)) * np.exp(-(t / t_phi)) / 2
    pi = 1 - (px + py + pz)
    print('px: ', py, 'pz: ', pz, 'pi: ', pi)
    A = np.zeros((pow(4, n), pow(2, n), pow(2, n)), dtype=complex)  # 3 dimensional array to store kraus matrices
    ptaOperators = {
        '0': np.sqrt(pi) * g.id(),
        '1': np.sqrt(px) * g.x(),
        '2': np.sqrt(py) * g.y(),
        '3': np.sqrt(pz) * g.z()
    }

    # get labels
    labels = op.createlabel(n, 4)

    for i in range(len(labels)):
        temp = 1
        for digit in labels[i]:
            temp = np.kron(temp, ptaOperators[digit])
        A[i] = temp
    return A


def pta_ad(n, t, t1):
    """
    Produces the kraus matrices for the pta channel
    :param n: number of qubit
    :param t: time step for evolution
    :param t1: relaxation time
    :return: returns a 3 dimensinal array of pta kraus matrices
    """
    gamma = 1 - np.exp(-t / t1)
    px = py = gamma / 4.0
    pz = 1.0 / 2.0 - py - np.sqrt(1 - gamma) / 2
    pi = 1 - (px + py + pz)
    A = np.zeros((pow(4, n), pow(2, n), pow(2, n)), dtype=complex)  # 3 dimensional array to store kraus matrices
    ptaOperators = {
        '0': np.sqrt(pi) * g.id(),
        '1': np.sqrt(px) * g.x(),
        '2': np.sqrt(py) * g.y(),
        '3': np.sqrt(pz) * g.z()
    }

    # get labels
    labels = op.createlabel(n, 4)

    for i in range(len(labels)):
        temp = 1
        for digit in labels[i]:
            temp = np.kron(temp, ptaOperators[digit])
        A[i] = temp
    return A


def kraus_ad(n, t, t1):
    """
      Produces the kraus matrices for the amplitude damping channel
        :param n: number of qubit
        :param t: time step for evolution
        :param t1: relaxation time
        :return: returns a 3 dimensinal array of amplitude damping kraus matrices
      """

    A = np.zeros((pow(2, n), pow(2, n), pow(2, n)), dtype=complex)  # 3 dimensional array to store kraus matrices
    gamma = 1 - np.exp(-t / t1)
    adOperators = {
        "0": np.array([[1, 0], [0, np.sqrt(1 - gamma)]]),
        "1": np.array([[0, np.sqrt(gamma)], [0, 0]])
    }

    labels = op.createlabel(n, 2)

    for i in range(len(labels)):
        temp = 1
        for digit in labels[i]:
            temp = np.kron(temp, adOperators[digit])
        A[i] = temp
    return A


def kraus_exact(n, t, t1, t2, markovian=False, alpha=None):
    """
    Produces the kraus matrices for the exact evolution of amplitude damping with dephasing channel
        :param n: number of qubit
        :param t: time step for evolution
        :param t1: relaxation time
        :param t2: dephasing time must be smaller than t1
        :param markovian: If true the kraus matrices are for non markovian evolution and
        t2 takes the role of  t_phi
        :param alpha: The power of 1/f^{alpha} flux noise
        :return:  a 3 dimensinal array of kraus matrices with amplitude damping and dephasing

    """
    A = np.zeros((pow(3, n), pow(2, n), pow(2, n)), dtype=complex)  # 3 dimensional array to store kraus matrices
    gamma = 1 - np.exp(-t / t1)
    if markovian:
        t_phi = 1 / t2 - 1 / (2 * t1)
        lambda1 = np.exp(-t / t1) * (1 - np.exp(-2 * (t / t_phi)))
        print('We are markovian')
    else:
        print('We are non markovian')
        t_phi = t2
        lambda1 = np.exp(-t / t1) * (1 - np.exp(-2 * (t / t_phi) ** (1 + alpha)))

    krausOperators = {
        "0": np.array([[1, 0], [0, np.sqrt(1 - gamma - lambda1)]]),
        "1": np.array([[0, np.sqrt(gamma)], [0, 0]]),
        "2": np.array([[0, 0], [0, np.sqrt(lambda1)]]),
    }

    labels = op.createlabel(n, 3)

    for i in range(len(labels)):
        temp = 1
        for digit in labels[i]:
            temp = np.kron(temp, krausOperators[digit])
        A[i] = temp

    return A


def generic_kraus(n, classical_error=False, opers=[], prob_error=[], generator=False):
    """
    This functions takes as an input generic operators and outputs a corresponding list of kraus operators for those
    n qubits. It also can do a classical simulation of noise by throwing down errors classically
    :param n:  The number of qubits experiencing the noise
    :param classical_error: If True the user must supply list of probabilities for list in oper
    :param opers: The list of kraus operators that appear in the sum
    :param prob_error: The list of probabilities for each operator in oper. Entries must add to 1. First operator is
    returned with probability in first position of prob_error.
    :param generator: Function becomes a generator in order to save memeory when a large number of qubits is being used
    :return:
    """

    num_operators = len(opers)

    if classical_error is False:
        A = np.zeros((pow(num_operators, n), pow(2, n), pow(2, n)),
                     dtype=complex) # 3 dimensional array to store kraus matrices
        kraus_operators = {str(i): opers[i] for i in range(len(opers))}
        labels = op.createlabel(n, num_operators)

        for i in range(len(labels)):
            temp=1
            for digit in labels[i]:
                temp = np.kron(temp, kraus_operators[digit])
            A[i] = temp
        return A

    if classical_error:
        # Returns a 3 dimensional array which stores only one kraus matrix
        A = np.zeros((pow(num_operators, 0), pow(2, n), pow(2, n)),
                     dtype=complex)  # 3 dimensional array to store kraus matrices
        if len(prob_error) != 0 or len(prob_error) != len(opers):
            if math.isclose(sum(prob_error), 1, rel_tol=1e-4):
                operators = {i: prob_error[i]*100 for i in range(len(prob_error))}
                lea_object = pmf(operators)
                picked_operator = lea_object.random()
                A[0] = opers[picked_operator]
                return A
            else:
                raise Exception('Probabilities must add to 1')
        else:
            raise Exception('prob_error list is empty or does not equal oper list')


def kraus_generator(n, non_ideal_qubits=0, classical_error=False, partialbath=False, opers=[]):
    """
    :param n:
    :param classical_error: Applies pauli noise stochastically
    :param opers: List of single kraus operators
    :param partialbath: Boolean variable if true kraus operators with identities on a subset of qubits will be produced
    :param non_ideal_qubits: The number of qubits that will decohere. It need not be all of them
    :return:
    """
    num_operators = len(opers)
    kraus_operators = {str(i): opers[i] for i in range(len(opers))}
    if classical_error is False and partialbath is False:
        labels = op.createlabel(n, num_operators)
        for i in range(len(labels)):
            kraus = 1
            for digit in labels[i]:
                kraus = np.kron(kraus, kraus_operators[digit])
            yield kraus
    elif classical_error is False and partialbath:
        labels = op.createlabel(non_ideal_qubits, num_operators)
        for i in range(len(labels)):
            kraus = 1
            for digit in labels[i]:
                kraus = np.kron(kraus, kraus_operators[digit])
            yield kraus


def apply_kraus(K, rho_s, n, non_ideal_qubits=0, partial_bath=False):
    """
    :param K: A python generator that produces kraus operators
    :param rho_s: density matrix of system
    :param non_ideal_qubits: The qubits that will decohere (need not be all of them)
    :param partial_bath: Boolean variable, if true only a subset of qubits will decohere
    :param n: Number of qubits
    :return: Return evolved density matrix
    """
    out = np.zeros((pow(2, n), pow(2, n)), dtype=complex)
    if partial_bath:
        ideal_qubits_oper = {'0': g.id()}
        id_oper = op.superkron(ideal_qubits_oper, val=1, string='0' * (n - non_ideal_qubits))
        for kraus in K:
            new_kraus = op.superkron(kraus, id_oper)
            out += np.dot(new_kraus, np.dot(rho_s, op.ctranspose(new_kraus)))
        return out
    else:
        for kraus in K:
            out += np.dot(kraus, np.dot(rho_s, op.ctranspose(kraus)))
        return out


if __name__ == '__main__':
    state = op.superkron(g.b4(), g.b4())
    state_1 = op.superkron(g.b4(), g.b4())
    E = [np.array([[1, 0], [0, np.cos(np.pi / 5)]]), np.array([[0, np.sin(np.pi / 5)], [0, 0]])]

    kraus = generic_kraus(2, classical_error=False, opers=E)
    m = [op.superkron(kraus[i]) for i in range(len(kraus))]

    for i in range(4):
        print(i)
        generator_kraus = kraus_generator(2, non_ideal_qubits=1, partialbath=True, classical_error=False, opers=E)
        state = apply_kraus(generator_kraus, state, 2, non_ideal_qubits=1, partial_bath=True)
        print('New Method:', state)

    for i in range(4):
        state_1 = serial_decohere(m, state_1, 2)
        print('Old Method: ', state_1)