
import numpy as sci
import matplotlib.pyplot as plt
import pandas



# Create function to assign seat number to each passenger
def AssignSeats(rq, cq, assign_type, ac):
    n_rows = ac.n_rows
    n_pass = ac.n_pass
    n_cols = ac.n_cols

    def arrangeIA(ia: list):
        p = []
        i = 0
        length_p = len(ia)
        while len(ia) > 0:
            if min(ia) != None:
                p.append(min(ia))
                ia.remove(min(ia))
            if (len(ia) == 0):
                continue
            if max(ia) != None:
                p.append(max(ia))
                ia.remove(max(ia))
            i += 2
        return p
    if (assign_type == "IA"):
        # Initialize initial and final positions
        i = 0
        f = ac.n_rows


        # Define column seating positions


        c = arrangeIA(list(sci.arange(0, n_cols, 1)))

        # Define iteratiion counter
        count = 0

        # Assign queue
        while (f <= n_pass):
            rq[i:f] = list(reversed(range(0, n_rows)))
            cq[i:f] = [c[count]] * n_rows
            i += n_rows
            f += n_rows
            count += 1

    if (assign_type == "Random"):
        av_rows = sci.arange(0, n_rows, 1)
        av_rows = sci.tile(av_rows, (n_cols, 1))
        av_rows = av_rows.T.flatten()
        av_cols = sci.arange(0, n_cols, 1)
        av_cols = sci.tile(av_cols, (n_rows, 1)).flatten()
        av_seats = sci.zeros((n_pass, 2))
        for i in range(n_pass):
            av_seats[i] = [av_rows[i], av_cols[i]]
        sci.random.shuffle(av_seats)
        rq = av_seats[:, 0]
        cq = av_seats[:, 1]

    if (assign_type == "BTF"):
        av_rows = sci.arange(0, n_rows, 1)
        av_rows = sci.tile(av_rows, (n_cols, 1))
        av_rows = av_rows.T.flatten()
        av_cols = sci.arange(0, n_cols, 1)
        av_cols = sci.tile(av_cols, (n_rows, 1)).flatten()
        av_seats = sci.zeros((n_pass, 2))
        for i in range(n_pass):
            av_seats[i] = [av_rows[i], av_cols[i]]
        group1 = av_seats[:48]
        sci.random.shuffle(group1)
        group2 = av_seats[48:96]
        sci.random.shuffle(group2)
        group3 = av_seats[96:]
        sci.random.shuffle(group3)
        av_seats_final = sci.concatenate((group3, group2, group1))
        rq = av_seats_final[:, 0]
        cq = av_seats_final[:, 1]

    if (assign_type == "FTB"):
        av_rows = sci.arange(0, n_rows, 1)
        av_rows = sci.tile(av_rows, (n_cols, 1))
        av_rows = av_rows.T.flatten()
        av_cols = sci.arange(0, n_cols, 1)
        av_cols = sci.tile(av_cols, (n_rows, 1)).flatten()
        av_seats = sci.zeros((n_pass, 2))
        for i in range(n_pass):
            av_seats[i] = [av_rows[i], av_cols[i]]
        group1 = av_seats[:48]
        sci.random.shuffle(group1)
        group2 = av_seats[48:96]
        sci.random.shuffle(group2)
        group3 = av_seats[96:]
        sci.random.shuffle(group3)
        av_seats_final = sci.concatenate((group1, group2, group3))
        rq = av_seats_final[:, 0]
        cq = av_seats_final[:, 1]

    if (assign_type == "WMA"):
        window_1 = sci.array([0] * n_rows)
        rows_1 = sci.arange(0, n_rows, 1)
        window_2 = sci.array([n_cols -1] * n_rows)
        rows_2 = sci.arange(0, n_rows, 1)
        window = sci.concatenate((window_1, window_2))
        rows = sci.concatenate((rows_1, rows_2))
        av_seats_w = sci.column_stack((rows, window))
        sci.random.shuffle(av_seats_w)

        aisle_1 = sci.array([n_cols/2 -1] * n_rows)
        aisle_2 = sci.array([n_cols/2] * n_rows)
        aisle = sci.concatenate((aisle_1, aisle_2))
        av_seats_a = sci.column_stack((rows, aisle))
        sci.random.shuffle(av_seats_a)

        col_array = list(sci.arange(0, n_cols, 1))
        arranged_array = arrangeIA(col_array)
        arranged_array = arranged_array[2:(len(arranged_array) - 2)]
        middle_list = []
        middle:sci.ndarray
        rows_m: sci.ndarray
        first_run = True
        for i in range(0,len(arranged_array)):
            middle_1 = sci.array([arranged_array[i]] * n_rows)
            middle_list.append(middle_1)
            if first_run:
                middle = middle_1
                rows_m = sci.arange(0, n_rows, 1)
                first_run = False
            else:
                middle = sci.concatenate((middle, middle_1))
                rows_m = sci.concatenate((rows_m, sci.arange(0, n_rows, 1)))



        av_seats_m = sci.column_stack((rows_m, middle))
        sci.random.shuffle(av_seats_m)

        av_seats = sci.concatenate((av_seats_w, av_seats_m, av_seats_a))
        rq = av_seats[:, 0]
        cq = av_seats[:, 1]

    if (assign_type == "Southwest"):
        # Make an array [0,5,0,5,...]
        window = sci.array([0, n_cols-1] * n_rows)

        # Make an array [0,0,1,1,2,2,...]
        rows_1 = sci.arange(0, n_rows, 1)
        rows_2 = sci.arange(0, n_rows, 1)
        rows = sci.ravel(sci.column_stack((rows_1, rows_2)))

        w_seats = sci.column_stack((rows, window))
        w_group1 = w_seats[:32, :]
        w_group2 = w_seats[32:, :]

        aisle = sci.array([(n_cols/2 - 1), n_cols/2] * n_rows)
        a_seats = sci.column_stack((rows, aisle))
        a_group1 = a_seats[:32, :]
        a_group2 = a_seats[32:, :]

        mega_group1 = sci.concatenate((w_group1, a_group1))
        sci.random.shuffle(mega_group1)
        mega_group2 = sci.concatenate((w_group2, a_group2))
        sci.random.shuffle(mega_group2)

        w_and_a = sci.concatenate((mega_group1, mega_group2))

        col_array = list(sci.arange(0, n_cols, 1))
        arranged_array = arrangeIA(col_array)
        arranged_array = arranged_array[2:(len(arranged_array) - 2)]

        middle = sci.array(arranged_array * n_rows)

        first_run = True
        for i in range(0, len(arranged_array)):
            if first_run:
                rows_m = sci.arange(0, n_rows, 1)
                first_run = False
            else:
                rows_m = sci.concatenate((rows_m, sci.arange(0, n_rows, 1)))


        m_seats = sci.column_stack((rows_m, middle))
        m_group1 = m_seats[:32, :]
        sci.random.shuffle(m_group1)
        m_group2 = m_seats[32:, :]
        sci.random.shuffle(m_group2)

        av_seats = sci.concatenate((w_and_a, m_group1, m_group2))
        rq = av_seats[:, 0]
        cq = av_seats[:, 1]


    return rq, cq


class Aircraft():
    def __init__(self):
        pass

    def Initialize(self, em: int = 1, am: int = 4, mm:  int = 5, amm: int = 7, rows = 23, cols = 6):
        # Initialize zero arrays
        # Define number of rows and columns
        self.n_rows = rows
        self.n_cols = cols

        # Calculate number of passengers
        self.n_pass = self.n_rows * self.n_cols

        # Create seat matrix
        self.seats = sci.zeros((self.n_rows, self.n_cols))
        self.seats[:, :] = -1

        # Create aisle array
        self.aisle_q = sci.zeros(self.n_rows)
        self.aisle_q[:] = -1

        # Create initial passenger number queue
        self.pass_q = [int(i) for i in range(self.n_pass)]
        self.pass_q = sci.array(self.pass_q)

        # Create array for seat nos
        self.row_q_init = sci.zeros(self.n_pass)
        self.col_q_init = sci.zeros(self.n_pass)

        # Define multipliers
        self.empty_mult = em + 2
        self.aisle_mult = am + 2
        self.middle_mult = mm + 2
        self.aisle_middle_mult = amm + 2

        # Let's create moveto arrays
        moveto_loc = sci.zeros(self.n_pass)
        moveto_time = sci.zeros(self.n_pass)

        self.moveto_loc_dict = {i: j for i in self.pass_q for j in moveto_loc}
        self.moveto_time_dict = {i: j for i in self.pass_q for j in moveto_time}

    def IssueSeatingOrder(self, assign_type,mean_time = 1, stddev_time = 0.2):
        # Assign seating order
        self.row_q, self.col_q = AssignSeats(self.row_q_init, self.col_q_init, assign_type, self)


        # Create seat and speed dictionary
        self.pass_dict = {}
        self.time_dict = {}

        # Create array for speeds
        self.time_q = sci.random.normal(loc=mean_time, scale=stddev_time, size=self.n_pass)

        seat_nos = sci.column_stack((self.row_q, self.col_q))
        for i in range(self.n_pass):
            self.pass_dict[i] = seat_nos[i]

        for i in range(self.n_pass):
            self.time_dict[i] = self.time_q[i]

        # Create sum time array
        self.sum_time = sci.zeros(self.n_pass)
        for i in range(self.n_pass):
            self.sum_time[i] = sum(self.time_q[:i + 1])


# Create function to move passengers into aircraft
def MoveToAisle(t, aisle_q, pass_q, sum_time):
    if (t > sum_time[0]):
        if (aisle_q[0] == -1):
            aisle_q[0] = pass_q[0].copy()
            pass_q = sci.delete(pass_q, 0)
            sum_time = sci.delete(sum_time, 0)
    return aisle_q, pass_q, sum_time


# Let's define the boarding process in a while loop
# Define initial conditions
def BoardFlight(ac):
    ac.time = 0
    n_iter = 0
    time_step = 0.1
    exit_sum = sci.sum(ac.pass_q)
    pass_sum = sci.sum(ac.seats)

    # Imaging definitions
    ac.img_list = []
    iters_per_snap = 50

    while (pass_sum != exit_sum):
        # Try to move passenger inside the plane if passengers are left
        if (ac.pass_q.size != 0):
            ac.aisle_q, ac.pass_q, sum_time = MoveToAisle(ac.time, ac.aisle_q, ac.pass_q, ac.sum_time)
        # Scan the aisle first for non-negative units (passengers)
        for passg in ac.aisle_q:
            if (passg != -1):
                # Store the row of passenger in aisle
                row = int(sci.where(ac.aisle_q == passg)[0][0])
                # See if move has been assigned to passenger
                if (ac.moveto_time_dict[passg] != 0):
                    # If move has been assigned check if it is time to move
                    if (ac.time > ac.moveto_time_dict[passg]):
                        # If it is time to move follow the procedure below
                        # Check if move is forward in aisle or to seat
                        if (ac.moveto_loc_dict[passg] == "a"):
                            # If move is in the aisle, check if position ahead is empty
                            if (ac.aisle_q[row + 1] == -1):
                                # If position is empty move passenger ahead and free the position behind
                                ac.aisle_q[row + 1] = passg
                                ac.aisle_q[row] = -1
                                # Set moves to 0 again
                                ac.moveto_loc_dict[passg] = 0
                                ac.moveto_time_dict[passg] = 0
                        elif (ac.moveto_loc_dict[passg] == "s"):
                            # If move is to the seat,
                            # Find seat row and column of passenger
                            passg_row = int(ac.pass_dict[passg][0])
                            passg_col = int(ac.pass_dict[passg][1])
                            # Set seat matrix position to the passenger number
                            ac.seats[passg_row, passg_col] = passg
                            # Free the aisle
                            ac.aisle_q[row] = -1
                elif (ac.moveto_time_dict[passg] == 0):
                    # If move hasn't been assgined to passenger
                    # Check passenger seat location
                    passg_row = int(ac.pass_dict[passg][0])
                    passg_col = int(ac.pass_dict[passg][1])
                    if (passg_row == row):
                        # If passenger at the row where his/her seat is,
                        # Designate move type as seat
                        ac.moveto_loc_dict[passg] = "s"
                        # Check what type of seat: aisle, middle or window
                        # Depending upon seat type, designate when it is time to move
                        col_list = list(sci.arange(0, ac.n_cols, 1))
                        col_list_1 = col_list[:int((ac.n_cols/2)+1)]
                        col_list_2 = col_list[int((ac.n_cols/2)+1):]
                        tta = 2 + 1


                        if(passg_col <= len(col_list)/2):
                            col_trim_list = col_list_1[passg_col:]
                            rev_list = col_trim_list
                            rev_list.reverse()
                            for i in range(0,len(rev_list)):
                                if ac.seats[passg_row, rev_list[i]] != -1:
                                    tta = tta + 4+i
                            if(tta > 5):
                                tta = int(float(tta)/1.28)
                            ac.moveto_time_dict[passg] = ac.time + tta* ac.time_dict[passg]
                        else:
                            col_trim_list = col_list_2[:passg_col]
                            for i in range(0, len(col_trim_list)):
                                if ac.seats[passg_row, col_trim_list[i]] != -1:
                                    tta = tta + 4 + i
                            if (tta > 8):
                                tta = int(float(tta) / 1.28)
                            ac.moveto_time_dict[passg] = ac.time + tta * ac.time_dict[passg]


                    elif (passg_row != row):
                        # If passenger is not at the row where his/her seat is,
                        # Designate movement type as aisle
                        ac.moveto_loc_dict[passg] = "a"
                        # Designate time to move
                        ac.moveto_time_dict[passg] = ac.time + ac.time_dict[passg]

        # Imaging
        if (n_iter % iters_per_snap == 0 and ac.repeat == 1):
            snap = ac.seats.copy()
            snap = sci.insert(snap, 3, ac.aisle_q, axis=1)
            ac.img_list.append(snap)

        # Iteration timekeeping
        ac.time += time_step
        n_iter += 1
        pass_sum = sci.sum(ac.seats)

    # Image final seat matrix
    if (ac.repeat == 1):
        snap = ac.seats.copy()
        snap = sci.insert(snap, 3, ac.aisle_q, axis=1)
        ac.img_list.append(snap)




# Run the simulation
def RunSimulation(rows,cols,mean_time,stddev_time,iterations):
    # Define aircraft object
    ac = Aircraft()

    # Define dict to store times
    time_dict = {
        "WMA": [],
        "Southwest": [],
        "BTF": [],
        "FTB": [],
        "IA": [],
        "Random": [],
    }

    # Boarding Methods to Compare
    methods = [
        "WMA",
        "Southwest",
        "BTF",
        "FTB",
        "IA",
        "Random"
    ]

    ac.repeat = iterations

    for method in methods:
        time_arr = []
        for i in range(ac.repeat):
            ac.Initialize(cols=cols, rows=rows)
            ac.IssueSeatingOrder(method, stddev_time=stddev_time, mean_time=mean_time)
            BoardFlight(ac)
            time_arr.append(ac.time)
        time_dict[method] = time_arr
        at = sum(time_arr) / len(time_arr)
        print("Average Time for " + method + " is " + str(at))
        time_dict[method].insert((len(time_arr)), at)

    # Print the result
    print(time_dict)
    best_time = ["", 0]
    for method in methods:

        if best_time[1] == 0:
            best_time[0] = method
            best_time[1] = time_dict[method][-1]
        elif best_time[1] > time_dict[method][-1]:
            best_time[0] = method
            best_time[1] = time_dict[method][-1]
        # print("The mean time for method " + method + " is " + str(time_dict[method]))
    print("The best method is " + best_time[0] + " with time " + str(best_time[1]))
    return time_dict


