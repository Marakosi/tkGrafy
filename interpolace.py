import scipy.interpolate as inp
import pylab as lab

#x = [0, 0.3, 0.5, 0.8, 1,  2,  3 ]
#y = [0, 0.1, 0.5, 1,   3, 10, 30]

x = "0 0.3 0.5 0.8 1  2  3".split()
y = "0 0.1 0.5 1   3 10 30".split()

x = list(map(float, x))
y = list(map(float, y))

spl = inp.CubicSpline(x, y)

newX = lab.linspace(0, 3, 20)
newY = spl(newX)

lab.plot(x, y)
lab.plot(newX, newY, '.')
lab.show()
