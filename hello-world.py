# Import the Qiskit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QiskitError
from qiskit import execute, IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy


# Authenticate for access to remote backends
try:
    IBMQ.load_accounts()
except:
    print("""WARNING: There's no connection with the API for remote backends.
             Have you initialized a file with your personal token?
             For now, there's only access to local simulator backends...""")

try:
    # Create a Quantum Register with 2 qubits.
    q = QuantumRegister(2)
    # Create a Classical Register with 2 bits.
    c = ClassicalRegister(2)
    # Create a Quantum Circuit
    qc = QuantumCircuit(q, c)

    # Add a H gate on qubit 0, putting this qubit in superposition.
    qc.h(q[0])
    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1, putting
    # the qubits in a Bell state.
    qc.cx(q[0], q[1])
    # Add a Measure gate to see the state.
    qc.measure(q, c)

    # See a list of available local simulators
    print("Simuladores Disponibles: ", BasicAer.backends())
    backend_sim = BasicAer.get_backend('qasm_simulator')

    # Compile and run the Quantum circuit on a simulator backend
    job_sim = execute(qc, backend_sim)
    result_sim = job_sim.result()

    # Show the results
    print('Resultado: {}'.format(str(result_sim.get_counts(qc))))

    print('Estado: {}'.format(job_sim.status()))
    # see a list of available remote backends
    ibmq_backends = IBMQ.backends()

    print("Simuladores Remotos: ", ibmq_backends)
    # Compile and run the Quantum Program on a real device backend
    try:
        least_busy_device = least_busy(IBMQ.backends(simulator=False))
        print("Corriendo el simulador: ", least_busy_device)

        #running the job
        job_exp = execute(qc, least_busy_device, shots=1024, max_credits=10)
        result_exp = job_exp.result()

        # Show the results
        print(result_exp.get_counts(qc))

    except:
        print("Actualmente ningun dispositivo esta disponible.")

except QiskitError as ex:
    print('Error = {}'.format(ex))
