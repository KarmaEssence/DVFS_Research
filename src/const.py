
# ------------ Generation parameters ------------------------------ */
b = 1e9  # Number of instructions per task.
CPI = 1  # Number of cycles per instruction received by the processor.
C = 20   # Number of cores of the processor (i.e. servers).
B = 45   # Maximal number of tasks in the waiting queue.
Type = 1 # 0 : Do not count the energy at startup, 1 : Count the energy at startup

# ------------ Energetic parameters : case of AMD Opteron processors --------------------- */

fi = [1e9, 1.8 * 1e9, 2 * 1e9, 2.2 * 1e9, 2.4 * 1e9, 2.6 * 1e9] # Frequency in GHz.
Mu = [float(f / (b * CPI)) for f in fi] # Service rate per step (i.e frequency).
en = [32, 55, 65, 76, 90, 95] # Energy consumption of an active server per step.
en_idle = [e/4 for e in en]   # Energy consumption of an idle server per step (75% of reduction).
Es = en                       # switch cost for each pstate (switch from pstate i to pstate i+1).
