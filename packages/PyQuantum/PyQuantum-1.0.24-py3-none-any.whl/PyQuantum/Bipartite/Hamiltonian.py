# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# -------------------------------------------------------------------------------------------------
# system
from math import sqrt
from PyQuantum.Common.html import *
import copy
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.Matrix import *
from PyQuantum.Common.Assert import *
from PyQuantum.Common.Print import *
# from PyQuantum.Common.ext import cf, print_error
# -------------------------------------------------------------------------------------------------
import html
import pandas as pd
import webbrowser


class Hamiltonian:

    # ---------------------------------------------------------------------------------------------
    def __init__(self, capacity, cavity):
        self.cavity = cavity

        self.D = {}

        count = 0

        M = capacity
        self.n = n = cavity.n
        wc = cavity.wc
        wa = cavity.wa
        g = cavity.g

        _min = min(M, n)

        self.states = {}

        # ---------------------------------------
        for i1 in range(0, _min + 1):
            for i2 in range(0, min(n, M - i1) + 1):
                self.states[count] = [i1, i2]

                count += 1
        # ---------------------------------------

        self.size = len(self.states)
        self.matrix = Matrix(self.size, self.size, dtype=np.complex128)

        i = 1

        for i1 in range(0, _min + 1):
            for i2 in range(0, min(n, M - i1) + 1):
                j = 1

                for j1 in range(0, _min + 1):
                    for j2 in range(0, min(n, M - j1) + 1):
                        if i1 != j1:
                            p = [i1, j1]
                        elif i2 != j2:
                            p = [i2, j2]
                        else:
                            p = [1, 2]

                        mi = min(p[0], p[1])

                        kappa = sqrt((n - mi) * (mi + 1))

                        if abs(i1 - j1) + abs(i2 - j2) == 1:
                            _max = max(M - i1 - i2, M - j1 - j2)
                            self.matrix.data[i - 1, j - 1] = g * \
                                sqrt(max(M - i1 - i2, M - j1 - j2)) * kappa
                        elif abs(i1 - j1) + abs(i2 - j2) == 0:
                            self.matrix.data[i - 1, j -
                                             1] = (M - (i1 + i2)) * wc + (i1 + i2) * wa
                        else:
                            self.matrix.data[i - 1, j - 1] = 0

                        j += 1

                i += 1

        # self.data = self.matrix.data
        # self.size = np.shape(self.data)[0]
        # self.print_states()
        # print(len(self.states), np.shape(self.data))
        # exit(1)

    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def get_index(self, state):
        for k, v in self.states.items():
            if v == state:
                return k
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def write_to_file(self, filename):
        self.matrix.write_to_file(filename)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def get_states(self):
        return self.states
    # ---------------------------------------------------------------------------------------------

    def print_html(self, filename):
        f = open(filename, "w")

        # html = """            <!DOCTYPE html>
        #     <html>
        #         <head>
        #             <title>
        #                 States
        #             </title>
        #         </head>

        #         <body>
        #             <table border=1>
        #     """
        # html += "<tr>"        html += "<td>"        html += "</td>"
        # # for i in range(0, len(self.states)):
        # #     html += "<td>"        #     html += "[" + str(self.states[i].n1) + "," + str(self.states[i].n2) + "]"        #     html += "</td>"
        # # html += "</tr>"
        # # for i in range(0, len(self.states)):
        # #     html += "<tr>"        #     html += "<td>"        #     html += "[" + str(self.states[i].n1) + "," + str(self.states[i].n2) + "]"        #     html += "</td>"
        # #     for j in range(0, len(self.states)):
        # #         html += "<td>"
        # #         if sqrt:
        # #             html += "&radic;" + "<span style="text-decoration:overline;">" + str(abs(self.matrix.data[i, j]) / self.g) + "</span>"        #         else:
        # #             html += "&radic;" + "<span style="text-decoration:overline;">" + str(abs(self.matrix.data[i, j])) + "</span>"
        # #         html += "</td>"
        # #     html += "</tr>"
        # html += """                    </table>
        #         </body>
        #     </html>
        #     """
        # f.write(html)
        f.close()

        webbrowser.open(filename)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # def init_states(self):
    #     self.states = []

    #     s = St(self.cavity)

    #     self.states.append(copy.copy(s))

    #     while(s.inc()):
    #         self.states.append(copy.copy(s))
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def print_states(self):
        print("States:", color="green")

        print()

        for k, v in self.states.items():
            print(v)

        print()
    # ---------------------------------------------------------------------------------------------


class St:

    def __init__(self, cv):
        self.capacity = cv.capacity
        self.n = cv.n

        self.n1 = 0
        self.n2 = 0

    def inc(self):
        if self.n2 < self.n and self.n1 + self.n2 < self.capacity:
            self.n2 += 1
        else:
            self.n2 = 0

            if self.n1 < self.n and self.n1 + self.n2 < self.capacity:
                self.n1 += 1
            else:
                return False

        return True

    def print(self):
        print("[" + str(self.n1) + "," + str(self.n2) + "]")
