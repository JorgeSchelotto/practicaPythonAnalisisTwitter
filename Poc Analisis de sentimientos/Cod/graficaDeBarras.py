import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure("Sensacion Twitter")
grupo1 = fig.add_subplot(111)
# grupo2 = fig.add_subplot(212)

alums1 = ["Positivos", "Neutrales", "Negativos"]
calif1 = np.array([7.8, 5.9, 8.0])

grupo1.bar(alums1, calif1, align="center")
grupo1.set_xticks(alums1)
grupo1.set_xticklabels(alums1)
#grupo1.set_yticklabels(calif1)
grupo1.set_ylabel("SCORE PROMEDIADo")


plt.show()