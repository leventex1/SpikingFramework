import numpy as np
import matplotlib.pyplot as plt

# Parameters for simulation
total_time = 100  # in ms
dt = 10  # time step in ms
tau = 20  # time constant in ms
V_initial = 1  # initial potential normalized to 1

time = np.arange(0, total_time, dt)

num_samples = min(14, len(time)-1)
# Adding an excitatory stimulus at time step 35
stimulus_time = 30
stimulus_value = 0.5

# Generate random sample points with the initial time point included
np.random.seed(10)  # for reproducibility
sample_points = np.sort(np.append([0, stimulus_time], np.random.choice(time[1:], size=num_samples, replace=False)))

# Initialize the sampled membrane potential array
V_sampled_with_stimulus = np.zeros_like(sample_points, dtype=float)
V_sampled_with_stimulus[0] = V_initial  # initial membrane potential at time 0

# Calculate membrane potential with stimulus added at time step 35
stimuli_applied = False
for i in range(1, len(sample_points)):
    delta_t = sample_points[i] - sample_points[i-1]
    V_sampled_with_stimulus[i] = V_sampled_with_stimulus[i-1] * np.exp(-delta_t / tau)

    if (sample_points[i] >= stimulus_time) and not stimuli_applied:
        V_sampled_with_stimulus[i] += stimulus_value
        stimuli_applied = True

    
V = np.zeros_like(time, dtype=float)
V[0] = V_initial
for i in range(1, len(time)):    
    delta_t = dt
    V[i] = V[i-1] * np.exp(-delta_t / tau)

    if time[i] == stimulus_time:
        V[i] += stimulus_value

# Plot the continuous decay, sampled points, and the effect of the stimulus
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
# Continuous decay plot
axes[0].plot(time, V, label=r"$V[i] = V[i-1] \times e^{-\Delta t/\tau}$")
axes[0].set_title("Continuous Membrane Potential Decay")
axes[0].set_xlabel("Time (ms)")
axes[0].set_ylabel("Membrane Potential (normalized)")
axes[0].set_ylim(0, 1.1)
axes[0].grid(True)
axes[0].legend()

# Sampled points plot with stimulus effect
axes[1].plot(time, V, label="Continuous Decay", color='lightgray', linestyle='--')
axes[1].scatter(sample_points, V_sampled_with_stimulus, color='red', label="Sampled Points with Stimulus")
axes[1].set_title("Membrane Potential Decay with Excitatory Stimulus at 35 ms")
axes[1].set_xlabel("Time (ms)")
axes[1].set_ylabel("Membrane Potential (normalized)")
axes[1].set_ylim(0, 1.1)
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()
