import control as ctl
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

window = tk.Tk()
window.title('Testando somente')
# button = ttk.Button(window, text = 'Sair', command = window.destroy)
# button.grid(row=3, column=0, pady=10)

def stringToArray(num, den):
    numArr = num.split()
    denArr = den.split()

    numArrInt = list(map(int, numArr))
    denArrInt = list(map(int, denArr))

    return numArrInt, denArrInt

def verifyValues(num, den):
    for element in num:
        if not element.isdigit() and not element == " ":
            errorLabel = tk.Label(window, text="São aceitos somente números e espaços")
            errorLabel.pack()
            return

    for element in den:
        if not element.isdigit() and not element == " ":
            errorLabel = tk.Label(window, text="São aceitos somente números e espaços")
            errorLabel.pack()
            return
    
    numArr, denArr = stringToArray(num, den)

    # numArr = np.array(numArr)
    # denArr = np.array(denArr)

    successLabel = tk.Label(window, text="Função de transferência criada com sucesso!")
    successLabel.pack(pady=10)

    buttonInitSimulation = ttk.Button(window, text="Iniciar simulação", command= lambda: generateGraphs(numArr, denArr))
    buttonInitSimulation.pack(pady=10)
    
def generateGraphs(numArr, denArr):
    system = ctl.TransferFunction(list(numArr), list(denArr))
    FTMFG = ctl.minreal(system / (1 + system))

    time_simulation = np.arange(0, 15, 0.05, dtype=float)
    xout, yout = ctl.step_response(FTMFG, time_simulation)

    # Criando subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
    # Primeiro gráfico
    ax1.plot(xout, yout)
    ax1.set_title('Step Response')

    # Segundo gráfico (por exemplo, o gráfico do sistema)
    ctl.rlocus(FTMFG, ax=ax2)
    ax2.set_title('Root Locus')

    # Configurando o layout
    fig.tight_layout()

    # Adicionando o gráfico à interface Tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def transferFunctionSelection():
    # for widget in window.winfo_children(): # ! funciona!!!
    #     widget.destroy()

    # if clickedTransferFunctionOptions.get() == '1° Grau':
    numLabel = tk.Label(window, text="Informe o numerador")
    numLabel.pack()
    num = tk.Entry(window, justify="center", width=10)
    num.pack()

    denLabel = tk.Label(window, text="Informe o(s) denominadores")
    denLabel.pack()
    den = tk.Entry(window, justify="center", width=10)
    den.pack()

    buttonSubmitTransferFunction = ttk.Button(window, text="Confirmar", command= lambda: verifyValues(num.get(), den.get()))
    buttonSubmitTransferFunction.pack(pady=10)


# def controlOptionsSelection(event):
#     if clickedControlOptions.get() == 'Ação proporcional':
#         gain = tk.Entry(window, justify="center", width=5)
#         gain.pack()

controlOptions = [
    "Nenhuma ação de controle",
    "Ação proporcional",
    "Ação integral",
    "Ação derivativa",
    "Ação proporcional-integral",
    "Ação proporcional-derivativa",
    "Ação proporcional-integrativa-derivativa"
]

# transferFunctionOptions = [
#     "1° Grau",
#     "2° Grau"    
# ]

# clickedControlOptions = tk.StringVar()
# clickedControlOptions.set(controlOptions[0])
# dropControlOptions = tk.OptionMenu(window, clickedControlOptions, *controlOptions, command=controlOptionsSelection)
# dropControlOptions.pack(pady=10)

# clickedTransferFunctionOptions = tk.StringVar()
# clickedTransferFunctionOptions.set(transferFunctionOptions[0])
# dropTransferFunctionsOptions = tk.OptionMenu(window, clickedTransferFunctionOptions, *transferFunctionOptions, command=transferFunctionSelection)
# dropTransferFunctionsOptions.pack(pady=10)

transferFunctionSelection()






window.mainloop()


# button = ttk.Button(window, text = 'Sair', command = window.destroy)
# button.grid(row=3, column=0, pady=10)





# num = np.array([25])
# den = np.array([1, 6, 25])
# gain = 1

# system = ctl.TransferFunction(num, den)
# FTMFG = ctl.minreal((gain * system) / (1 + (gain * system)))

# time_simulation = np.arange(0, 15, 0.05, dtype=float)

# [xout, yout] = ctl.step_response(FTMFG, time_simulation)

# plt.figure()
# ctl.rlocus(FTMFG)
# plt.show()

# plt.figure()
# plt.plot(xout, yout)
# plt.show()