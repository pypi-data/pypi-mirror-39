#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import itertools

import numpy
import pytest
import scipy

import cirq
import openfermion

from openfermioncirq.gates import (
        DoubleExcitation, DoubleExcitationGate, CombinedDoubleExcitationGate)

from openfermioncirq.gates.four_qubit_gates import (
        state_swap_eigen_component)


def test_state_swap_eigen_component_args():
    with pytest.raises(TypeError):
        state_swap_eigen_component(0, '12', 1)
    with pytest.raises(ValueError):
        state_swap_eigen_component('01', '01', 1)
    with pytest.raises(ValueError):
        state_swap_eigen_component('01', '10', 0)
    with pytest.raises(ValueError):
        state_swap_eigen_component('01', '100', 1)
    with pytest.raises(ValueError):
        state_swap_eigen_component('01', 'ab', 1)


@pytest.mark.parametrize('index_pair,n_qubits', [
    ((0, 1), 2),
    ((0, 3), 2),
    ])
def test_state_swap_eigen_component(index_pair, n_qubits):
    state_pair = tuple(format(i, '0' + str(n_qubits) + 'b') for i in index_pair)
    i, j = index_pair
    dim = 2 ** n_qubits
    for sign in (-1, 1):
        actual_component = state_swap_eigen_component(
                state_pair[0], state_pair[1], sign)
        expected_component = numpy.zeros((dim, dim))
        expected_component[i, i] = expected_component[j, j] = 0.5
        expected_component[i, j] = expected_component[j, i] = sign * 0.5
        assert numpy.allclose(actual_component, expected_component)


def test_double_excitation_repr():
    assert repr(DoubleExcitationGate(exponent=1)) == 'DoubleExcitation'
    assert repr(DoubleExcitationGate(
        exponent=0.5)) == 'DoubleExcitation**0.5'


def test_double_excitation_init_with_multiple_args_fails():
    with pytest.raises(ValueError):
        _ = DoubleExcitationGate(exponent=1.0, duration=numpy.pi/2)


def test_double_excitation_eq():
    eq = cirq.testing.EqualsTester()

    eq.add_equality_group(DoubleExcitationGate(exponent=1.5),
                          DoubleExcitationGate(exponent=-0.5),
                          DoubleExcitationGate(rads=-0.5 * numpy.pi),
                          DoubleExcitationGate(degs=-90),
                          DoubleExcitationGate(duration=-0.5 * numpy.pi / 2))

    eq.add_equality_group(DoubleExcitationGate(exponent=0.5),
                          DoubleExcitationGate(exponent=-1.5),
                          DoubleExcitationGate(rads=0.5 * numpy.pi),
                          DoubleExcitationGate(degs=90),
                          DoubleExcitationGate(duration=-1.5 * numpy.pi / 2))

    eq.make_equality_group(lambda: DoubleExcitationGate(exponent=0.0))
    eq.make_equality_group(lambda: DoubleExcitationGate(exponent=0.75))


@pytest.mark.parametrize('exponent', [1.0, 0.5, 0.25, 0.1, 0.0, -0.5])
def test_double_excitation_decompose(exponent):
    cirq.testing.assert_decompose_is_consistent_with_unitary(
            DoubleExcitation**exponent)


def test_apply_unitary():
    cirq.testing.assert_has_consistent_apply_unitary_for_various_exponents(
        DoubleExcitation,
        exponents=[1, -0.5, 0.5, 0.25, -0.25, 0.1, cirq.Symbol('s')],
        qubit_count=4)

    cirq.testing.assert_has_consistent_apply_unitary_for_various_exponents(
        CombinedDoubleExcitationGate(weights=(0.2, 0.3, 0.4)),
        exponents=[1, -0.5, 0.5, 0.25, -0.25, 0.1, cirq.Symbol('s')],
        qubit_count=4)


@pytest.mark.parametrize('weights', numpy.random.rand(10, 3))
def test_weights_and_exponent(weights):
    exponents = numpy.linspace(-1, 1, 8)
    gates = tuple(
            CombinedDoubleExcitationGate(weights / exponent,
                                         exponent=exponent)
            for exponent in exponents)

    cirq.testing.EqualsTester().add_equality_group(*gates)

    for i, (gate, exponent) in enumerate(zip(gates, exponents)):
        assert gate.exponent == 1
        new_exponent = exponents[-i]
        new_gate = gate._with_exponent(new_exponent)
        assert new_gate.exponent == new_exponent


double_excitation_simulator_test_cases = [
        (DoubleExcitation, 1.0,
         numpy.array([1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         numpy.array([1, 1, 1, -1, 1, 1, 1, 1,
                      1, 1, 1, 1, -1, 1, 1, 1]) / 4.,
         5e-6),
        (DoubleExcitation, -1.0,
         numpy.array([1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         numpy.array([1, 1, 1, -1, 1, 1, 1, 1,
                      1, 1, 1, 1, -1, 1, 1, 1]) / 4.,
         5e-6),
        (DoubleExcitation, 0.5,
         numpy.array([1, 1, 1, 1, 1, 1, 1, 1,
                      0, 0, 0, 0, 0, 0, 0, 0]) / numpy.sqrt(8),
         numpy.array([1, 1, 1, 0, 1, 1, 1, 1,
                      0, 0, 0, 0, 1j, 0, 0, 0]) / numpy.sqrt(8),
         5e-6),
        (DoubleExcitation, -0.5,
         numpy.array([1, -1, -1, -1, -1, -1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         numpy.array([1, -1, -1, -1j, -1, -1, 1, 1,
                      1, 1, 1, 1, 1j, 1, 1, 1]) / 4.,
         5e-6),
        (DoubleExcitation, -1. / 7,
         numpy.array([1, 1j, -1j, -1, 1, 1j, -1j, -1,
                      1, 1j, -1j, -1, 1, 1j, -1j, -1]) / 4.,
         numpy.array([1, 1j, -1j,
                      -numpy.cos(numpy.pi / 7) - 1j * numpy.sin(numpy.pi / 7),
                      1, 1j, -1j, -1, 1, 1j, -1j, -1,
                      numpy.cos(numpy.pi / 7) + 1j * numpy.sin(numpy.pi / 7),
                      1j, -1j, -1]) / 4.,
         5e-6),
        (DoubleExcitation, 7. / 3,
         numpy.array([0, 0, 0, 2,
                      (1 + 1j) / numpy.sqrt(2), (1 - 1j) / numpy.sqrt(2),
                      -(1 + 1j) / numpy.sqrt(2), -1,
                      1, 1j, -1j, -1,
                      1, 1j, -1j, -1]) / 4.,
         numpy.array([0, 0, 0, 1 + 1j * numpy.sqrt(3) / 2,
                      (1 + 1j) / numpy.sqrt(2), (1 - 1j) / numpy.sqrt(2),
                      -(1 + 1j) / numpy.sqrt(2), -1,
                      1, 1j, -1j, -1,
                      0.5 + 1j * numpy.sqrt(3), 1j, -1j, -1]) / 4.,
         5e-6),
        (DoubleExcitation, 0,
         numpy.array([1, -1, -1, -1, -1, -1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         numpy.array([1, -1, -1, -1, -1, -1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         5e-6),
        (DoubleExcitation, 0.25,
         numpy.array([1, 0, 0, -2, 0, 0, 0, 0,
                      0, 0, 0, 0, 3, 0, 0, 1]) / numpy.sqrt(15),
         numpy.array([1, 0, 0, +3j / numpy.sqrt(2) - numpy.sqrt(2),
                      0, 0, 0, 0,
                      0, 0, 0, 0,
                      3 / numpy.sqrt(2) - 1j * numpy.sqrt(2), 0, 0, 1]) /
         numpy.sqrt(15),
         5e-6)
    ]
combined_double_excitation_simulator_test_cases = [
        (CombinedDoubleExcitationGate((0, 0, 0)), 1.,
         numpy.ones(16) / 4.,
         numpy.ones(16) / 4.,
         5e-6),
        (CombinedDoubleExcitationGate((0.2, -0.1, 0.7)), 0.,
         numpy.array([1, -1, -1, -1, -1, -1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         numpy.array([1, -1, -1, -1, -1, -1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         5e-6),
        (CombinedDoubleExcitationGate((0.2, -0.1, 0.7)), 0.3,
         numpy.array([1, -1, -1, -1, -1, -1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1]) / 4.,
         numpy.array([1, -1, -1, -numpy.exp(-numpy.pi * 0.105j),
                      -1, -numpy.exp(-numpy.pi * 0.585j),
                      numpy.exp(numpy.pi * 0.03j), 1,
                      1, numpy.exp(numpy.pi * 0.03j),
                      numpy.exp(-numpy.pi * 0.585j), 1,
                      numpy.exp(-numpy.pi * 0.105j), 1, 1, 1]) / 4.,
         5e-6),
        (CombinedDoubleExcitationGate((1. / 3, 0, 0)), 1.,
         numpy.array([0, 0, 0, 0, 0, 0, 1., 0,
                      0, 1., 0, 0, 0, 0, 0, 0]) / numpy.sqrt(2),
         numpy.array([0, 0, 0, 0, 0, 0, 1., 0,
                      0, 1., 0, 0, 0, 0, 0, 0]) / numpy.sqrt(2),
         5e-6),
        (CombinedDoubleExcitationGate((0, -2. / 3, 0)), 1.,
         numpy.array([1., 1., 0, 0, 0, 1., 0, 0,
                      0, 0., -1., 0, 0, 0, 0, 0]) / 2.,
         numpy.array([1., 1., 0, 0, 0, -numpy.exp(4j * numpy.pi / 3), 0, 0,
                      0, 0., -numpy.exp(1j * numpy.pi / 3), 0, 0, 0, 0, 0]
                     ) / 2.,
         5e-6),
        (CombinedDoubleExcitationGate((0, 0, 1)), 1.,
         numpy.array([0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 1., 0, 0, 0]),
         numpy.array([0, 0, 0, 1, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0]),
         5e-6),
        (CombinedDoubleExcitationGate((0, 0, 0.5)), 1.,
         numpy.array([0, 0, 0, 1, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0]),
         numpy.array([0, 0, 0, 1, 0, 0, 0, 0,
                      0, 0, 0, 0, 1j, 0, 0, 0]) / numpy.sqrt(2),
         5e-6),
        (CombinedDoubleExcitationGate((0.5, -1./3, 1.)), 1.,
         numpy.array([0, 0, 0, 0, 0, 0, 1, 0,
                      0, 0, 1, 0, 1, 0, 0, 0]) / numpy.sqrt(3),
         numpy.array([0, 0, 0, 1j, 0, -1j / 2., 1 / numpy.sqrt(2), 0,
                      0, 1j / numpy.sqrt(2), numpy.sqrt(3) / 2, 0, 0, 0, 0, 0]
                     ) / numpy.sqrt(3),
         5e-6),
        ]
@pytest.mark.parametrize(
    'gate, exponent, initial_state, correct_state, atol',
    double_excitation_simulator_test_cases +
    combined_double_excitation_simulator_test_cases)
def test_four_qubit_rotation_gates_on_simulator(
        gate, exponent, initial_state, correct_state, atol):

    a, b, c, d = cirq.LineQubit.range(4)
    circuit = cirq.Circuit.from_ops(gate(a, b, c, d)**exponent)
    result = circuit.apply_unitary_effect_to_state(initial_state)
    cirq.testing.assert_allclose_up_to_global_phase(
        result, correct_state, atol=atol)


def test_double_excitation_gate_text_diagrams():
    a = cirq.NamedQubit('a')
    b = cirq.NamedQubit('b')
    c = cirq.NamedQubit('c')
    d = cirq.NamedQubit('d')

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(a, b, c, d))
    cirq.testing.assert_has_diagram(circuit, """
a: ───⇅───
      │
b: ───⇅───
      │
c: ───⇵───
      │
d: ───⇵───
""")

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(a, b, c, d)**-0.5)
    cirq.testing.assert_has_diagram(circuit, """
a: ───⇅────────
      │
b: ───⇅────────
      │
c: ───⇵────────
      │
d: ───⇵^-0.5───
""")

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(a, c, b, d)**0.2)
    cirq.testing.assert_has_diagram(circuit, """
a: ───⇅───────
      │
b: ───⇵───────
      │
c: ───⇅───────
      │
d: ───⇵^0.2───
""")

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(d, b, a, c)**0.7)
    cirq.testing.assert_has_diagram(circuit, """
a: ───⇵───────
      │
b: ───⇅───────
      │
c: ───⇵───────
      │
d: ───⇅^0.7───
""")

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(d, b, a, c)**2.3)
    cirq.testing.assert_has_diagram(circuit, """
a: ───⇵───────
      │
b: ───⇅───────
      │
c: ───⇵───────
      │
d: ───⇅^0.3───
""")


def test_double_excitation_gate_text_diagrams_no_unicode():
    a = cirq.NamedQubit('a')
    b = cirq.NamedQubit('b')
    c = cirq.NamedQubit('c')
    d = cirq.NamedQubit('d')

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(a, b, c, d))
    cirq.testing.assert_has_diagram(circuit, """
a: ---/\ \/---
      |
b: ---/\ \/---
      |
c: ---\/ /\---
      |
d: ---\/ /\---
""", use_unicode_characters=False)

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(a, b, c, d)**-0.5)
    cirq.testing.assert_has_diagram(circuit, """
a: ---/\ \/--------
      |
b: ---/\ \/--------
      |
c: ---\/ /\--------
      |
d: ---\/ /\^-0.5---
""", use_unicode_characters=False)

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(a, c, b, d)**0.2)
    cirq.testing.assert_has_diagram(circuit, """
a: ---/\ \/-------
      |
b: ---\/ /\-------
      |
c: ---/\ \/-------
      |
d: ---\/ /\^0.2---
""", use_unicode_characters=False)

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(d, b, a, c)**0.7)
    cirq.testing.assert_has_diagram(circuit, """
a: ---\/ /\-------
      |
b: ---/\ \/-------
      |
c: ---\/ /\-------
      |
d: ---/\ \/^0.7---
""", use_unicode_characters=False)

    circuit = cirq.Circuit.from_ops(
        DoubleExcitation(d, b, a, c)**2.3)
    cirq.testing.assert_has_diagram(circuit, """
a: ---\/ /\-------
      |
b: ---/\ \/-------
      |
c: ---\/ /\-------
      |
d: ---/\ \/^0.3---
""", use_unicode_characters=False)


@pytest.mark.parametrize('exponent', [1.0, 0.5, 0.25, 0.1, 0.0, -0.5])
def test_double_excitation_matches_fermionic_evolution(exponent):
    gate = DoubleExcitation ** exponent

    op = openfermion.FermionOperator('3^ 2^ 1 0')
    op += openfermion.hermitian_conjugated(op)
    matrix_op = openfermion.get_sparse_operator(op)

    time_evol_op = scipy.linalg.expm(-1j * matrix_op * exponent * numpy.pi)
    time_evol_op = time_evol_op.todense()

    cirq.testing.assert_allclose_up_to_global_phase(
        cirq.unitary(gate), time_evol_op, atol=1e-7)


def test_combined_double_excitation_repr():
    weights = (0, 0, 0)
    gate = CombinedDoubleExcitationGate(weights)
    assert (repr(gate) == 'CombinedDoubleExcitation(0.0, 0.0, 0.0)')

    weights = (0.2, 0.6, -0.4)
    gate = CombinedDoubleExcitationGate(weights)
    assert (repr(gate) == 'CombinedDoubleExcitation(0.2, 0.6, 3.6)')

    gate **=0.5
    assert (repr(gate) == 'CombinedDoubleExcitation(0.1, 0.3, 1.8)')

def test_combined_double_excitation_init_with_multiple_args_fails():
    with pytest.raises(ValueError):
        _ = CombinedDoubleExcitationGate(
                (1,1,1), exponent=1.0, duration=numpy.pi/2)


def test_combined_double_excitation_eq():
    eq = cirq.testing.EqualsTester()

    eq.add_equality_group(
            CombinedDoubleExcitationGate((1.2, 0.4, -0.4), exponent=0.5),
            CombinedDoubleExcitationGate((0.3, 0.1, -0.1), exponent=2),
            CombinedDoubleExcitationGate((-0.6, -0.2, 0.2), exponent=-1),
            CombinedDoubleExcitationGate((0.6, 0.2, 3.8)),
            CombinedDoubleExcitationGate(
                (1.2, 0.4, -0.4), rads=0.5 * numpy.pi),
            CombinedDoubleExcitationGate((1.2, 0.4, -0.4), degs=90),
            CombinedDoubleExcitationGate(
                (1.2, 0.4, -0.4), duration=0.5 * numpy.pi / 2)
            )

    eq.add_equality_group(
            CombinedDoubleExcitationGate((-0.6, 0.0, 0.3), exponent=0.5),
            CombinedDoubleExcitationGate((0.2, -0.0, -0.1), exponent=-1.5),
            CombinedDoubleExcitationGate((-0.6, 0.0, 0.3),
                                         rads=0.5 * numpy.pi),
            CombinedDoubleExcitationGate((-0.6, 0.0, 0.3), degs=90),
            CombinedDoubleExcitationGate((-0.2, 0.0, 0.1),
                                         duration=1.5 * numpy.pi / 2)
            )

    eq.make_equality_group(
            lambda: CombinedDoubleExcitationGate(
                (0.1, -0.3, 0.0), exponent=0.0))
    eq.make_equality_group(
            lambda: CombinedDoubleExcitationGate(
                (1., -1., 0.5), exponent=0.75))


def test_combined_double_excitation_gate_text_diagram():
    gate = CombinedDoubleExcitationGate((1,1,1))
    qubits = cirq.LineQubit.range(6)
    circuit = cirq.Circuit.from_ops(
            [gate(*qubits[:4]), gate(*qubits[-4:])])

    actual_text_diagram = circuit.to_text_diagram()
    expected_text_diagram = """
0: ───⇊⇈────────
      │
1: ───⇊⇈────────
      │
2: ───⇊⇈───⇊⇈───
      │    │
3: ───⇊⇈───⇊⇈───
           │
4: ────────⇊⇈───
           │
5: ────────⇊⇈───
    """.strip()
    assert actual_text_diagram == expected_text_diagram

    actual_text_diagram = circuit.to_text_diagram(use_unicode_characters=False)
    expected_text_diagram = """
0: ---a*a*aa------------
      |
1: ---a*a*aa------------
      |
2: ---a*a*aa---a*a*aa---
      |        |
3: ---a*a*aa---a*a*aa---
               |
4: ------------a*a*aa---
               |
5: ------------a*a*aa---
    """.strip()
    assert actual_text_diagram == expected_text_diagram


test_weights = [1.0, 0.5, 0.25, 0.1, 0.0, -0.5]
@pytest.mark.parametrize('weights', itertools.chain(
        itertools.product(test_weights, repeat=3),
        numpy.random.rand(10, 3)
        ))
def test_combined_double_excitation_decompose(weights):
    cirq.testing.assert_decompose_is_consistent_with_unitary(
            CombinedDoubleExcitationGate(weights))
