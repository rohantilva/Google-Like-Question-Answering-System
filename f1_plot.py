mport matplotlib.pyplot as plt
x = [0, 1, 2, 3]
y = [0.09, 0.12, 0.16, 0.18]

plt.plot(x, y, marker='o', color='b')

plt.xlabel('Project Timeline')
plt.ylabel('F1')
plt.title('F1 Scores over Time')
plt.xticks([0, 1, 2, 3], ['\nSVM with tf-idf cosine-sim', '\nStop word filtering', '\nMLP with question word feature', '\nMLP with all features and\n subtractive balance mod'])


plt.show()

