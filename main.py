# importing libraies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# function for job entry
def IntArr_serv(x):
    z = np.random.randint(1, 10, x)
    y = np.random.randint(1, 10, x)
    return list(z), list(y)

# input of the user
x = IntArr_serv(int(input("Please Enter the number of Jobs: ")))

# variables
IntArr = x[0]
service = x[1]
time = 0
arrTime = []
delay = [0]
completion = []
begin = []
wait_node = []
idleT = [0]
Qt = [0]
Xt = [1]
Lt = []

# get the arrival times from inter arrival time input
for i in IntArr:
    time += i
    arrTime.append(time)

# computing (completion/wait in node/delay/service begin) times
completion.append(arrTime[0] + service[0])
for i in range(0, len(arrTime)):
    if arrTime[i+1] >= completion[-1]:
        completion.append(arrTime[i+1] + service[i+1])
        delay.append(0)
        idleT.append(int(arrTime[i+1] - completion[i]))
    else:
        delay.append(int(completion[-1] - arrTime[i+1]))
        completion.append(arrTime[i+1] + delay[-1] + service[i+1])
        idleT.append(0)
    if i == len(arrTime)-2:
        break
wait_node = [sum(tup) for tup in zip(delay, service)]
begin = [sum(tup) for tup in zip(arrTime, delay)]


# computing Q(t)/X(t)/L(t)
for i in range(len(arrTime)):
    if arrTime[i+1] > completion[i]:
        Xt.append(0)
        Qt.append(0)
    elif arrTime[i+1] == completion[i]:
        Xt.append(1)
        Qt.append(0)
    else:
        Qt.append(int(Qt[-1])+1)
        Xt.append(1)
    if i == len(arrTime)-2:
        break
Lt = [sum(tup) for tup in zip(Qt, Xt)]

# calculating summary
totalJob = len(arrTime)
finalclock = int(completion[-1])
n_wait = 0
dx = 5 # duration of interval in curve
for i in delay:
    if i != 0:
        n_wait += 1

a = sum(delay)/totalJob
b = n_wait/totalJob
c = sum(idleT)/finalclock
d = sum(service)/totalJob
e = sum(IntArr)/(totalJob-1)
f = sum(delay)/n_wait
g = sum(wait_node)/totalJob
h = np.trapz(Qt, dx=dx)/finalclock
i = np.trapz(Xt, dx=dx)/finalclock



# putting it all together in DataFrame
data = {'Inter_Arrival': IntArr, 'Arrival_time': arrTime, 'Delay(time_in_Q)': delay, 'Service_Begin': begin, 'Service_time': service,
        'Wait_node(t_in_sys)': wait_node, 'Completion_time': completion, 'Idle_time': idleT}
df = pd.DataFrame(data)

# Display DataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df.head(10))
if len(arrTime) > 10:

    q2 = input("Do you want to see the whole data? [Yes/No]: ")
    if q2 == 'y' or q2 == 'yes' or q2 == 'Y' or q2 == 'Yes' or q2 == 'YES':

        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.precision', 3,
                               ):
            print(df)
    else:
        print("_____continuing without the rest of the data______")

# printing summary
q1 = input("Show Summary results? [Yes/No]: ")
def show_res():
    print("Average Waiting Time: {:.2f} minutes".format(a))
    print("Probability (wait): {:.2f}%".format(b*100))
    print("Probability of idle server: {:.2f}%".format(c*100))
    print("Average Service Time: {:.2f} minutes".format(d))
    print("Average Time between Arrivals: {:.2f} minutes".format(e))
    print("Average Waiting Time in queue: {:.2f} minutes per job".format(f))
    print("Average Time job spent in the system: {:.2f} minutes".format(g))
    print("Time-Average number in queue: {:.2f} part".format(h))
    print("Utilization of drill press: {:.2f}".format(i))
if q1 == 'y' or q1 == 'yes' or q1 == 'Y' or q1 == 'Yes' or q1 == 'YES':
    show_res()
else:
    print("----------------------Summary Results is Skipped----------------------")
    
# visuals of Q(t)/X(t)/L(t)

def show_viz():
    interval = [str(i) for i in range(1, len(arrTime)+1)]
    plt.title("Q(t) curve")
    plt.bar(interval, Qt)
    plt.show()
    plt.title("X(t) curve")
    plt.bar(interval, Xt)
    plt.show()
    plt.title("L(t) curve")
    plt.bar(interval, Lt)
    plt.show()


answer = input("Display the Curves Visuals? [Yes/No]: ")
if answer == 'y' or answer == 'yes' or answer == 'Y' or answer == 'Yes' or answer == 'YES':
    show_viz()
    print("----------------------End of Simulation----------------------")
else:
    print("----------------------End of Simulation----------------------")
