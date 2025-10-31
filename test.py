import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt

# --- Config ---
N_QUBITS = 8
K_LAYERS = 3
SQUEEZENET_OUTPUT_DIM = 512
def count_total_params(nqbit, nlayer):
    total_params = 0
    for i in range(nlayer):
        n = nqbit
        if n < 2: continue
        n_conv = n
        per_layer = 15 * n_conv
        total_params += per_layer
        if i < nlayer - 1:
            sel_shape = qml.StronglyEntanglingLayers.shape(n_layers=1, n_wires=n)
            total_params += np.prod(sel_shape)
    return total_params

# --- Define custom conv10 block ---
def conv10(wires, weights):
    qml.Rot(weights[0], weights[1], weights[2], wires=wires[0])
    qml.Rot(weights[3], weights[4], weights[5], wires=wires[1])
    qml.CNOT(wires=[wires[0], wires[1]])
    qml.RX(weights[6], wires=wires[0])
    qml.RZ(weights[7], wires=wires[1])
    qml.CNOT(wires=[wires[1], wires[0]])
    qml.RY(weights[8], wires=wires[0])
    qml.CNOT(wires=[wires[0], wires[1]])
    qml.Rot(weights[9], weights[10], weights[11], wires=wires[0])
    qml.Rot(weights[12], weights[13], weights[14], wires=wires[1])

# --- Embedding ---
def PatchesEmbedding(features, n_wires):
    n_features_per_wire = SQUEEZENET_OUTPUT_DIM // n_wires
    n_extra_features = SQUEEZENET_OUTPUT_DIM % n_wires
    rotations = [qml.RX, qml.RY, qml.RZ]
    feature_idx = 0
    for i in range(n_wires):
        n_features = n_features_per_wire + (1 if i < n_extra_features else 0)
        for j in range(n_features):
            gate = rotations[j % len(rotations)]
            gate(features[feature_idx], wires=i)
            feature_idx += 1

# --- Observables ---
def obs_gen(n_qubits):
    pauli_operators = [qml.PauliX, qml.PauliY, qml.PauliZ]
    obs = []
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            for p_i in pauli_operators:
                for p_j in pauli_operators:
                    obs.append(p_i(i) @ p_j(j))
    return obs

ALL_OBSERVABLES = obs_gen(N_QUBITS)

# --- Quantum device ---
dev = qml.device("default.qubit", wires=N_QUBITS)

@qml.qnode(dev)
def quantum_circuit(inputs, q_weights):
    PatchesEmbedding(inputs, N_QUBITS)
    
    active_wires = list(range(N_QUBITS))
    weight_idx = 0
    for layer in range(K_LAYERS):
        n = len(active_wires)
        if n >= 2:
            seen = set()
            for i in range(n):
                a, b = active_wires[i], active_wires[(i + 1) % n]
                key_ = tuple(sorted((a, b)))
                if key_ not in seen:
                    conv_w = q_weights[weight_idx: weight_idx + 15]
                    conv10([a, b], conv_w)
                    weight_idx += 15
                    seen.add(key_)
            qml.Barrier()
            
            if layer < K_LAYERS - 1:
                sel_shape = qml.StronglyEntanglingLayers.shape(n_layers=1, n_wires=n)
                sel_param_size = int(np.prod(sel_shape))
                sel_params = q_weights[weight_idx: weight_idx + sel_param_size].reshape(sel_shape)
                qml.StronglyEntanglingLayers(weights=sel_params, wires=active_wires, ranges=[1])
                weight_idx += sel_param_size
                qml.Barrier()
    
    return [qml.expval(i) for i in ALL_OBSERVABLES]

# --- Run sample and draw circuit ---
inputs = np.random.uniform(0, np.pi, SQUEEZENET_OUTPUT_DIM)
q_weights = np.random.uniform(0, 2 * np.pi, count_total_params(nlayer=3, nqbit=8))
fig, ax = qml.draw_mpl(quantum_circuit)(inputs, q_weights)
fig.savefig("fig.png", bbox_inches="tight")
plt.close(fig)
print("✅ Circuit saved as fig.png")
