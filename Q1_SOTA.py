from numpy import pi, array, linspace
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

m = 1                               #set the mass
k = w**2*m                          #set the constant k
E = 1/2*k*x_0**2 + 1/2*m*v_0**2     #set initial energy
t = 0                               #initialize time variable
x_i, v_i = x_0, v_0                 #initialize pos. and vel. variables
a_i = -k*x_0 / m                    #set initial acceleration

values = [(t, x_0, v_0, a_i, E)]    #initialize list to store values

########################          Compute x(t)        ######################


for i in range(n):
    a_i = -k*x_i / m
    x_i += v_i * time_interval + 1/2 * a_i * time_interval**2
    a_i_plus_1 = -k*x_i / m
    v_i += 1/2 * (a_i + a_i_plus_1) * time_interval
    t += time_interval
    E = 1/2*k*x_i**2 + 1/2*m*v_i**2
    values.append((t, x_i, v_i, a_i, E))


#########################          Print x(t)        #######################


headers = ["Time", "Position", "Velocity", "Energy"]

for header in headers:
    print("{:<15}".format(header), end="")

print("")

for row in values:
    for column in [0, 1, 2, 4]:
        print("{:<15}".format(round(row[column], 4)), end="")
    print("")


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
plt.title('x(t)')

# show the plot
plt.show()
