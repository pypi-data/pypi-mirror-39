from qComputing import NoisyEvolution as ne
from qComputing import Operations as op
from scipy.linalg import expm
from qComputing import Gates as g
from lea import *
from qutip import *
from matplotlib.pyplot import *


class Qubit(object):
    """
    This class  defines an N-qubit system and implements closed dynamics or open system dynamics
    assuming existence of kraus operators. For a linblad simulation use
    Qubitobj class.
    """

    def __init__(self, string, n, no_measurment_qubits=1, left_justified=False):
        """
        :param string: This should be a string of 1's and 0's where 1 is the |1> and
        0 is |0>
        :param n: The number of qubits in the system
        :param no_measurment_qubits:  The number of qubits that will be measured
        :return: Returns the

        Description of class variables
        state: This is the density matrix of the system
        classical_states: This is a dictionary of computational basis states that should have
        has its keys labels of computational basis states and values the corresponding
        probabilities
        no_measurement_qubits: The number of qubits you intend to measure
        classical_states_history: Has a key values all possible measurement syndromes and keeps a record of their
        probabilities
        single_kraus: These are the kraus operators used for a single qubit. They are used to create kraus operators
        for the n qubit system. This is assumed to be a dictionary containing kraus channels for single qubit i.e
        {'0': Amplitude damping , '1': De-phasing}
        partial_bath: This is aa boolean variable. If true some qubits the last m qubits on the left will not decohere
        no_non_ideal_qubits: These are the number of qubits, k that will decohere.  m+k must equal to n the number of
        qubits in the system
        hamiltonian: The hamiltonian of the system
        T: The total evolution time of the system
        state: The state of the quantum system for n qubits
        """
        self.oper_dict = {'0': g.b1(), '1': g.b4(), '2': g.id()}

        self.state = op.superkron(self.oper_dict, val=1, string=string)
        self.n = n
        self.no_measurement_qubits = no_measurment_qubits
        self.measurement_string = op.createlabel(self.no_measurement_qubits, 2)
        for i in range(len(self.measurement_string)):
            if left_justified:
                self.measurement_string[i] = self.measurement_string[i].ljust(self.n, '2')
            else:
                self.measurement_string[i] = self.measurement_string[i].rjust(self.n, '2')
        self.classical_states = {i.replace('2', ''): 0 for i in self.measurement_string}
        self.classical_states_history = {i.replace('2', ''): [] for i in self.measurement_string}
        self.hamiltonian = None
        self.dt = None
        self.U = None
        self.xlabel = ''
        self.ylabel = ''
        self.T = None
        self.kraus_operators = []
        self.expect_values = {}
        self.yield_kraus = None
        self.single_kraus = None
        self.partial_bath= False
        self.no_non_ideal_qubits = 0

    def get_projectors(self, measure_strings):
        """
        :param measure_strings: A label used to create a projection operator for a classical state
        :return: A generator that contains a projection operators
        """
        if isinstance(measure_strings, list):
            for i in measure_strings:
                yield op.superkron(self.oper_dict, val=1, string=i)

    def time_step_evolve(self, basis=''):
        """
        :param h: Hamiltonian by which to evolve the system
        :param dt: time step to evolve by could be small or large
        :param basis: Basis of measurement
        :return: returns the state of qubit after evolution
        """
        self.U = expm(-1j * self.hamiltonian * self.dt)
        self.state = np.dot(self.U, np.dot(self.state, op.ctranspose(self.U)))
        for state, projector in zip(self.classical_states, self.get_projectors(self.measurement_string)):
            # Possibly change basis of measurement before calculating probability history.
            self.measure_basis(pauli_string=basis)
            self.classical_states_history[state].append(np.trace(np.dot(self.state, projector)).real)
            self.measure_basis(pauli_string=basis, undo_basis=True)

    def q_decohere(self, k, n, parallel=False):
        """
        :param k: Kraus operators to be used
        :param n: Number of qubits in the system
        :param parallel: Boolean variable if true implements a parallel for loop else we just do non paralled kraus
        operators
        :return:
        """
        if parallel:
            self.state = ne.decohere(k, self.state, n)
        else:
            self.state = ne.serial_decohere(k, self.state, n)

    def evolve(self, basis=''):
        """
        :param basis: Basis in which we will do the measurement
        :return:
        """
        for i in np.arange(0, self.T, self.dt):
            # self.q_decohere(self.kraus_operators, self.n)
            self.time_step_evolve(basis=basis)
            self.qubits_decohere(self.n)

    def measure(self, return_state=False, basis='', nan_avoid=False, small_no=10**(-10)):
        """
        This performs a projective measurement on your n qubit system
        :param return_state: This is a boolean variable, if True it returns the label for
        :param basis: Basis in which to do the measurement. Must be an operator for pauli operator
        the classical state picked after projective measurement
        :param nan_avoid: Places  small_no in place of 0 probability in order to avoid divinding by 0
        :param small_no: The small number to replace 0
        :return:
        """

        # Calculate the probabilities for all classical states
        for state, projectors in zip(self.classical_states, self.get_projectors(self.measurement_string)):
            # Possibly change the basis for measurement, if basis is empty nothing should happen
            self.measure_basis(pauli_string=basis)
            self.classical_states[state] = np.trace(np.dot(self.state, projectors)).real
        # Make the probabilities of classical states into numbers between 0 and 100 for Lea
        outcomes = {state: self.classical_states[state] * 100 for state in self.classical_states}
        picked_obj = pmf(outcomes)
        picked_state = picked_obj.random()
        self.state = self.get_projectors([picked_state])

        if nan_avoid:
            for i in self.classical_states:
                if self.classical_states[i] == 0:
                    self.classical_states[i] = small_no
        if return_state:
            return picked_state

    def operator(self, o):
        """
        :param o: The operator you want applied to the qubit
        :return:  Returns the transformed density matrix after the operation
        """
        self.state = np.dot(o, np.dot(self.state, op.ctranspose(o)))

    def measure_basis(self, pauli_string='', undo_basis=False):
        """
        :param pauli_string: Basis in which to make the measurement
        :param undo_basis: Boolean variable
        :return:
        """
        measurement_operator = 1
        if pauli_string != '' and undo_basis is False:
            for char in pauli_string:
                if char == 'X':
                    measurement_operator = op.superkron(measurement_operator, g.r_y(-np.pi / 2))
                elif char == 'Y':
                    measurement_operator = op.superkron(measurement_operator, g.r_x(np.pi / 2))
                else:
                    measurement_operator = op.superkron(measurement_operator, g.id())
            self.operator(measurement_operator)
        elif pauli_string != '' and undo_basis is True:
            for char in pauli_string:
                if char == 'X':
                    measurement_operator = op.superkron(measurement_operator, g.r_y(np.pi / 2))
                elif char == 'Y':
                    measurement_operator = op.superkron(measurement_operator, g.r_x(-np.pi / 2))
                else:
                    measurement_operator = op.superkron(measurement_operator, g.id())
            self.operator(measurement_operator)
        else:
            pass

    def graph(self, state):
        """
        :param state: Classical state for which we wish to plot results
        :return:
        """
        xlabel(self.xlabel)
        ylabel(self.ylabel)
        t = [i for i in range(0, len(self.classical_states_history[state]))]
        plot(t, self.classical_states_history[state], label='|' + state + '>')
        ticklabel_format(axis='both', style='sci', scilimits=(-2, 2))
        legend()
        show()

    def expectation_values(self, operator_dict):
        """
        :param operator_dict: A dictionary of operators for which you need the expectation value of
        :return: A dictionary with the expectation values of the operators provided
        """
        if isinstance(operator_dict, dict):
            for i in operator_dict:
                self.expect_values[i] = np.trace(np.dot(self.state, operator_dict[i]))
        else:
            raise Exception('operator_dict must be a dictionary')

    def qubits_decohere(self, n_s):
        """
        :param n_s: The number of qubits in the system
        :return:
        """
        for m in self.single_kraus:
            K = ne.kraus_generator(n_s, non_ideal_qubits=self.no_non_ideal_qubits, classical_error=False, opers=self.single_kraus[m],
                               partialbath=self.partial_bath)
            self.state = ne.apply_kraus(K, self.state, n_s, non_ideal_qubits=self.no_non_ideal_qubits, partial_bath=self.partial_bath)


class QubitObj(object):
    """
    Does what the Qubit class does but with qutip stuff
    If you want to use qutip, this class automizes a lot of stuff
    Does a linblad equation simulation
    """

    def __init__(self, n, t1_list, t2_list, t3_list, string='', damp=True, phase_damp=True, finite_temp=False,
                 identical_bath=True):
        q0 = basis(2, 0)
        q1 = basis(2, 1)
        self.opt = Options(rhs_reuse=True, store_states=True)
        q_list = []
        q_list1 = []
        if isinstance(string, str):
            for c in string:
                if c == '0':
                    q_list.append(q0)
                    q_list1.append(q0 * q0.dag())
                    self.psi = tensor(*q_list)
                    self.rho = tensor(*q_list1)
                elif c == '1':
                    q_list.append(q1)
                    q_list1.append(q1 * q1.dag())
                    self.rho = tensor(*q_list1)
                    self.psi = tensor(*q_list)
        self.hamiltonian = 0
        self.psi_results = 0
        self.rho_results = 0
        self.operators = []
        self.c_op = {}
        self.dephase_op = {}
        self.create_op = {}
        self.collap = []
        self.x_label = ''
        self.y_label = ''
        self.label = ''
        self.x_axis = []
        self.y_axis = []
        self.n = n
        self.t1 = t1_list
        self.t2 = t2_list
        self.t3 = t3_list
        self.times = 0
        self.annihilate = {'0': qeye(2), '1': destroy(2)}
        self.create = {'0': qeye(2), '1': create(2)}
        self.dephase = {'0': qeye(2), '1': sigmaz()}
        self.final_state = 0
        for i in range(0, n):
            self.c_op[str(i)] = []
            self.create_op[str(i)] = []
            self.dephase_op[str(i)] = []
        self.noise_op(same_bath=identical_bath, relax=damp, dephase=phase_damp, create=finite_temp)

    def evolve(self):
        self.psi_results = mesolve(self.hamiltonian, self.psi, self.times, [], self.operators, options=self.opt)
        self.rho_results = mesolve(self.hamiltonian, self.rho, self.times, self.collap, self.operators,
                                   options=self.opt)
        self.final_state = self.rho_results.states[-1].full()

    def apply_op(self, op):
        self.psi = op * self.psi
        self.rho = op * self.rho * op.dag()

    def graph(self, *args):
        xlabel(self.x_label)
        ylabel(self.y_label)
        plot(*args, label=self.label)
        legend()
        show()

    def noise_op(self, same_bath=True, relax=True, dephase=False, create=False):
        noise_op_string_list = op.generatehamiltoniantring(self.n, '1')
        for qubit, string in enumerate(noise_op_string_list):
            for char in string:
                self.c_op[str(qubit)].append(self.annihilate[char])
                self.dephase_op[str(qubit)].append(self.dephase[char])
                self.create_op[str(qubit)].append(self.create[char])
        for q, q1, q2 in zip(self.c_op, self.dephase_op, self.create_op):
            if relax:
                self.c_op[q] = tensor(*self.c_op[q])
            if dephase:
                self.dephase_op[q1] = tensor(*self.dephase_op[q1])
            if create:
                self.create_op[q2] = tensor(*self.create_op[q2])
                self.collap.append(self.create_op[q2])
        if same_bath:
            if relax:
                for qs in self.c_op:
                    self.c_op[qs] = np.sqrt(1 / self.t1[0]) * self.c_op[qs]
                    self.collap.append(self.c_op[qs])
            if dephase:
                for qs in self.dephase_op:
                    self.dephase_op[qs] = np.sqrt(1 / (2 * self.t2[0])) * self.dephase_op[qs]
                    self.collap.append(self.dephase_op[qs])
            if create:
                for qs in self.dephase_op:
                    self.create_op[qs] = np.sqrt(1 / (self.t3[0])) * self.create_op[qs]
                    self.collap.append(self.create_op[qs])
        if same_bath is False:
            if relax:
                for t1_list, qs in enumerate(self.c_op):
                    self.c_op[qs] = np.sqrt(1 / self.t1[t1_list]) * self.c_op[qs]
                    self.collap.append(self.c_op[qs])
            if dephase:
                for t2_list, qs in enumerate(self.dephase_op):
                    self.dephase_op[qs] = np.sqrt(1 / (2 * self.t2[t2_list])) * self.dephase_op[qs]
                    self.collap.append(self.dephase_op[qs])
            if create:
                for t3_list, qs in enumerate(self.create_op):
                    self.create_op[qs] = np.sqrt(1 / self.t3[t3_list]) * self.create_op[qs]
                    self.collap.append(self.create_op[qs])


if __name__ == '__main__':
    # q = QubitObj(4, [0.5, 0.3], [0.5, 0.6], [10**(-9), 10**(-9)], string='1111',
    #              identical_bath=True)
    # q.times = np.linspace(0, 1, 10000)
    # q.hamiltonian = tensor(sigmaz(), sigmaz(), sigmaz(),sigmaz())
    # q.operators.append(tensor(sigmay(), sigmay(),sigmay(), sigmay()))
    # q.rho = ss.cluster_obj(4, density_matrix=True)
    # q.x_axis = q.times
    # q.evolve()
    # print(q.rho_results.expect[0])
    # q.y_axis = q.rho_results.expect[0]
    # q.label = 'Probability of $\sigma_z$'
    # q.graph(q.times, q.y_axis)
    n = 2
    init = '1'*n
    oper_dict = {'0': g.z()}
    E = [np.array([[1, 0], [0, np.cos(np.pi/5)]]), np.array([[0, np.sin(np.pi/5)], [0, 0]])]
    F = [np.array([[1, 0], [0, np.cos(np.pi/5)]]), np.array([[0, 0], [0, np.sin(np.pi/5)]])]
    kraus_op = {'0': E, '1': F}
    # k = ne.generic_kraus(1, classical_error=False, opers=E)
    # generator_kraus = ne.kraus_generator(1, classical_error=False, opers=E)
    # m = [op.superkron(k[i]) for i in range(len(k))]
    q2 = Qubit(init, n, no_measurment_qubits=n)
    q2.single_kraus = kraus_op
    q2.dt = 0.01
    q2.T = 1
    q2.partial_bath = True
    q2.no_non_ideal_qubits = n
    # k = ne.kraus_ad(q2.n, 0.001, 10 ** (-2))
    # k = ne.kraus_exact(q2.n, q2.dt, 10**(-6), 10**(-6), markovian=True)
    # q2.kraus_operators = m
    # q2.yield_kraus = generator_kraus
    q2.xlabel = 'time'
    q2.ylabel = 'Probability'
    q2.hamiltonian = 0.5*op.superkron(oper_dict, val=1, string='0'*n)
    q2.evolve(basis='Z'*n)
    # print('Returned state : ', q2.measure(return_state=True))
    # print('Probability distribution :', q2.classical_states)
    # q2.expectation_values({'X':op.superkron(g.z(), g.z(), g.z(), g.z(), g.z()), 'Y':op.superkron(g.y(), g.y(), g.y(), g.y(), g.y())})
    q2.graph('11')
    q2.graph('00')

    # print(q2.expect_values)
