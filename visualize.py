from boarding_simulation import Aircraft,AssignSeats
import numpy as sci
import matplotlib.pyplot as plt
def visualize(H):
    fig = plt.figure(figsize=(6, 8))
    ax = fig.add_subplot(111)
    ax.set_title('Seat Allotment')
    plt.imshow(H)
    ax.set_aspect('equal')

    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

ac = Aircraft()
methods = [
"WMA",
"Southwest",
"BTF",
"FTB",
"IA",
"Random"
]


ac.Initialize()
print("Which method do you want to visualize?")
print("""WMA",
"Southwest",
"BTF",
"FTB",
"IA",
"Random" """)
method_to_use = input()
rq,cq = AssignSeats(ac.row_q_init,ac.col_q_init,method_to_use,ac)
seat_matrix = sci.zeros((ac.n_rows, ac.n_cols))
for i in range(0,ac.n_pass):
    seat_matrix[int(rq[i]),int( cq[i])] = i
aisle = sci.zeros((ac.n_rows, 1))
target = sci.hstack((seat_matrix[:,:int((ac.n_cols/2))], aisle, seat_matrix[:,int(ac.n_cols/2):]))
visualize(target)
