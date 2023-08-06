from tkinter.filedialog import askopenfilename, Tk
from tkinter.simpledialog import askstring
from matplotlib import pyplot as plt
from matplotlib import style

import pandas as pd

Tk().withdraw()
filename = askopenfilename()
training_data = pd.read_csv(filename)

Tk().withdraw()
filename = askopenfilename()
validation_data = pd.read_csv(filename)

train, *_ = plt.plot(training_data.Step, training_data.Value, label='Traning')
val, *_ = plt.plot(validation_data.Step, validation_data.Value, label='Validation')

plt.legend(handles=[train, val])
name = askstring('Plot name', 'Plot name')
plt.title(f'{name}: Training + Validation')
y_name = askstring('Y name', 'Y Name')
plt.ylabel(y_name)
plt.xlabel('Epochs')

plt.show()
