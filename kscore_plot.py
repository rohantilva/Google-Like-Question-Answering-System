import  matplotlib.pyplot as plt

k = [1, 10, 100, 1000]
s_baseline = [0.0, 0.06, 0.18, 0.3]
s_query = [0.04, 0.32, 0.48, 0.64]
s_final = []

plt(k, s_baseline, 'r--', k, s_query, 'bs', k, s_final)

plt.show()

