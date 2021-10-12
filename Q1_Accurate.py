'''
The solution to the differential equation mx'' = -kx is of the form:

                        x = A sin(ωt + φ)

where A is the amplitude of the motion and w = sqrt(k/m). This python code 
uses the function "sin" from "numpy".
'''

from numpy import sin, pi, arctan, linspace, array
from colorama import Fore, Style
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def check(name, value):
    print(f"\t{Fore.RED}{name} set to {value}{Style.RESET_ALL}")
    return value

#####################      Set Initial Parameters      #####################

time_interval = check("Time Interval", float(input("Time interval: ")))

x_0 = check("Initial x", float(input("Initial position in m: ")))

v_0 = check("Initial v", float(input("Initial velocity in m/s: ")))

w_string = input("Angular frequency in rad/s (write \"pi\" to indicate π): ")
w_list = w_string.split("pi")
w = 1

for number in w_list:               #get rational part of ω
    if number:
        w *= int(number)

w_string = str(w) + "π" * bool(len(w_list) - 1)
if len(w_list) - 1 > 1:
    w_string += f"^{len(w_list) - 1}"
w *= pi**(len(w_list) - 1)
check("ω", w_string)


n = check("Number of Iterations", int(input("Number of iterations: ")))

########################          Compute x(t)        ######################
'''
We know that x(t) = A sin(ωt + φ) and v(t) = Aω cos(ωt + φ). Then, from the 
initial values:
                                  _
                                 |  v_0 = Aω cos(φ)     (1)
                                <
                                 |  x_0 = A sin(φ)      (2)
                                  ‾
Dividing (2) by (1), we obtain: tan(φ) = ω·x_0/v_0. Then:

                                    φ = arctan(ω·x_0/v_0)
                                    A = x_0/sin(φ)
'''

t , x = 0, x_0

if v_0 == 0:
    A = x_0
    phase = pi/2

else:
    phase = arctan(w*x_0/v_0)
    if phase < 0:
        phase += 2*pi
    A = x_0/sin(phase)

values = []

for iteration in range(n):
    values.append((t, x))
    t += time_interval
    x = A*sin(w*t+phase)


#########################          Print x(t)        #######################

print("Time", "\t", "Position")

for point in values:
    print(round(point[0], 4), "\t", round(point[1], 4))


#########################          Plot x(t)        #######################

# x and y axis values
x = [point[0] for point in values]
y = [point[1] for point in values]

# make a curve to fit the data
x = array(x)
y = array(y)
X_Y_Spline = make_interp_spline(x, y)
X_ = linspace(x.min(), x.max(), 500)
Y_ = X_Y_Spline(X_)
 
# plot the points
plt.plot(X_, Y_)
 
# name axes and set title
plt.xlabel('time (s)')
plt.ylabel('x (m)')
plt.title(f'x(t) = {round(A, 3)} · sin({w_string}t + {round(phase, 3)})')

# show the plot
plt.show()