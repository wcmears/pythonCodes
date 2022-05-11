import matplotlib.pyplot as plt
import math
x = range(0,90)
for b in range(0,100,5):
    a = b/100
    y = []
    for i in range(0,90):
        n = (a*math.sin(math.radians(i)))
        d = (1-(a*math.cos(math.radians(i))))
        v = n/d
        y.append(v)
    plt.plot(x, y, label = (str(b/100) + 'c'))
y = []
for i in range(0,90):
    y.append(1)
plt.plot(x, y, label = ('SLM Threshold'))
plt.xlabel('Angle of Inclination(Degrees)')
plt.ylabel('Beta Apparent')
plt.title('Apparent Velocity as Fraction of SOL vs. Angle of inclination for Various True Velocities')
plt.legend()
plt.show()