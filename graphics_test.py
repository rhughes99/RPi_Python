import matplotlib.pyplot as plt
import math

# Create sinewaves with sine and cosine
xs = [i / 5.0 for i in range(0, 50)]
y1s = [math.sin(x) for x in xs]
y2s = [math.cos(x) for x in xs]

# Plot both sinewaves on the same graph
plt.plot(xs, y1s, 'r^', label='sin(x)')
plt.plot(xs, y2s, 'b--', label='cos(x)')

# Adjust the axes' limits: [xmin, xmax, ymin, ymax]
plt.axis([-1, 11, -1.5, 1.5])

# Give the graph a title and axis labels
plt.title('My Sinewaves')
plt.xlabel('Radians')
plt.ylabel('Value')

# Show a legend
plt.legend()

# Save the image
plt.savefig('sinewaves.png')

# Draw to the screen
plt.show()
