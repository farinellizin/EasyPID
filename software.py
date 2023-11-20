from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import control as ctl
from tkinter import messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/farinellizin/Desktop/build/assets/frame0")

def stringToArray(num, den):
    numArr = num.split()
    denArr = den.split()

    numArrInt = list(map(int, numArr))
    denArrInt = list(map(int, denArr))

    return numArrInt, denArrInt

def verifyValues(num, den):
    for element in num:
        if not element.isdigit() and not element == " ":
            messagebox.showerror('Input Error', 'Only numeric values and spaces are accepted in the numerator input')
            return

    for element in den:
        if not element.isdigit() and not element == " ":
            messagebox.showerror('Input Error', 'Only numeric values and spaces are accepted in the denominator input')
            return
    
    numArr, denArr = stringToArray(num, den)
    return numArr, denArr

def plotWithoutControl(system, FTMF, den):
    time, response = ctl.step_response(FTMF)
    stepInfo = ctl.step_info(FTMF)
    
    time_simulation = np.arange(0, 15, 0.05, dtype=float)
    xout, yout = ctl.step_response(FTMF, time_simulation)

    # de fato plotar e inserir no tkinter # ! GRÁFICO DA RESPOSTA AO DEGRAU
    figure1 = plt.figure(figsize=(4, 4), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().place(x=450, y=10)
    ax1.plot(xout, yout)

    # de fato obter polos e inserir no tkinter # ! GRÁFICO DOS POLOS
    figure2 = plt.figure(figsize=(4, 4), dpi=100)
    roots, _ = ctl.root_locus(system, plot=True)
    bar2 = FigureCanvasTkAgg(plt.gcf(), window)
    bar2.get_tk_widget().place(x=950, y=10)

    # de fato obter bode e inserir no tkinter
    figure3 = plt.figure(figsize=(4, 4), dpi=100)
    ax3 = figure3.add_subplot(111)
    frequency = np.logspace(-1, 2, 100)
    _, mag, phase = ctl.bode_plot(system, omega=frequency, dB=True)
    ax3.semilogx(frequency, mag)
    bar3 = FigureCanvasTkAgg(figure3, window)
    bar3.get_tk_widget().place(x=1450, y=10)

    # Dados função de Transferência sem controle
    roots = np.roots(den)
    print(roots) # Polos # !

    maxPeakValue = np.max(response)
    print(maxPeakValue) # Máximo Valor de Pico

    # Instante de Pico
    peakTime = stepInfo['PeakTime']
    print(peakTime) # Instante do Valor de Pico

    # Tempo de estabilização
    settlingTime = stepInfo['SettlingTime']
    print(settlingTime) # Tempo de estabilização

    # Ultrapassagem percentual
    overshootPercentage = stepInfo['Overshoot']
    print(overshootPercentage) # Ultrapassagem percentual

    # Erro em regime permanente

    # Valor final
    finalValue = stepInfo['SteadyStateValue']
    print(finalValue) # Valor final

def plotWithControl(system, FTMF, den):
    time, response = ctl.step_response(FTMF)
    stepInfo = ctl.step_info(FTMF)

    time_simulation = np.arange(0, 15, 0.05, dtype=float)
    xout, yout = ctl.step_response(FTMF, time_simulation)

    # de fato plotar e inserir no tkinter # ! GRÁFICO DA RESPOSTA AO DEGRAU
    figure1 = plt.figure(figsize=(4, 4), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().place(x=450, y=500)
    ax1.plot(xout, yout)

    # de fato obter polos e inserir no tkinter # ! GRÁFICO DOS POLOS
    figure2 = plt.figure(figsize=(4, 4), dpi=100)
    roots, _ = ctl.root_locus(FTMF, plot=True)
    bar2 = FigureCanvasTkAgg(plt.gcf(), window)
    bar2.get_tk_widget().place(x=950, y=500)

    # de fato obter bode e inserir no tkinter
    figure3 = plt.figure(figsize=(4, 4), dpi=100)
    ax3 = figure3.add_subplot(111)
    frequency = np.logspace(-1, 2, 100)
    _, mag, phase = ctl.bode_plot(FTMF, omega=frequency, dB=True, plot=True)
    ax3.semilogx(frequency, mag)
    bar3 = FigureCanvasTkAgg(figure3, window)
    bar3.get_tk_widget().place(x=1450, y=500)

    # Dados função de Transferência sem controle
    roots = np.roots(den)
    print(roots) # Polos # !

    maxPeakValue = np.max(response)
    print(maxPeakValue) # Máximo Valor de Pico

    # Instante de Pico
    peakTime = stepInfo['PeakTime']
    print(peakTime) # Instante do Valor de Pico

    # Tempo de estabilização
    settlingTime = stepInfo['SettlingTime']
    print(settlingTime) # Tempo de estabilização

    # Ultrapassagem percentual
    overshootPercentage = stepInfo['Overshoot']
    print(overshootPercentage) # Ultrapassagem percentual

    # Erro em regime permanente

    # Valor final
    finalValue = stepInfo['SteadyStateValue']
    print(finalValue) # Valor final


def updateData():
    # if figure1 is not None and bar1 is not None: #! FUNCIONA.
    #     # Destrua o Canvas do primeiro gráfico
    #     bar1.get_tk_widget().destroy()

    if not entry_3.get() and entry_4.get() and entry_5.get():
        messagebox.showerror('PID Error', 'The combination integrative-derivative is not supported')
        return

    numeratorEntry = entry_1.get()
    denominatorEntry = entry_2.get()

    num, den = verifyValues(numeratorEntry, denominatorEntry)

    system = ctl.TransferFunction(num, den)
    FTMF = ctl.minreal(system / (1 + system))

    if entry_3.get() and not entry_4.get() and not entry_5.get(): # proporcional
        K = int(entry_3.get())
        FTMFP = ctl.minreal((K * system) / (1 + (K * system)))
        plotWithControl(system, FTMFP, den)
        
    elif not entry_3.get() and entry_4.get() and not entry_5.get(): # integrativa
        Ki = int(entry_4.get())
        integralController = ctl.TransferFunction(Ki, [1, 0])
        FTMFI = ctl.minreal((integralController * system) / (1 + (integralController * system)))
        plotWithControl(system, FTMFI, den)

    elif not entry_3.get() and not entry_4.get() and entry_5.get(): # derivativa
        Kd = int(entry_5.get())
        derivativeController = ctl.TransferFunction([Kd, 0], [1]) # ? perguntar thabatta
        FTMFD = ctl.minreal((derivativeController * system) / (1 + (derivativeController * system)))
        plotWithControl(system, FTMFD, den)

    elif entry_3.get() and entry_4.get() and not entry_5.get(): # proporcional - integrativa
        K = int(entry_3.get())
        Ki = int(entry_4.get())
        PIController = ctl.TransferFunction([K, Ki], [1, 0])
        FTMFPI = ctl.minreal((PIController * system) / (1 + (PIController * system)))
        plotWithControl(system, FTMFPI, den)

    elif entry_3.get() and not entry_4.get() and entry_5.get(): # proporcional - derivativa
        K = int(entry_3.get())
        Kd = int(entry_5.get())
        PDController = ctl.TransferFunction([K, Kd], [1])
        FTMFPD = ctl.minreal((PDController * system) / (1 + (PDController * system)))
        plotWithControl(system, FTMFPD, den)

    elif entry_3.get() and entry_4.get() and entry_5.get(): # proporcional - integrativa - derivativa
        K = int(entry_3.get())
        Ki = int(entry_4.get())
        Kd = int(entry_5.get())
        PIDController = ctl.TransferFunction([Kd, K, Ki], [1, 0])
        FTMFPID = ctl.minreal((PIDController * system) / (1 + (PIDController * system)))
        plotWithControl(system, FTMFPID, den)

    plotWithoutControl(system, FTMF, den)

    


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.title('Software')
window.geometry("1920x1080")
window.configure(bg = "#BC851C")

canvas = Canvas(
    window,
    bg = "#BC851C",
    height = 1080,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    400.0,
    1080.0,
    fill="#242424",
    outline="")

canvas.create_text(
    71.0,
    0.0,
    anchor="nw",
    text="Menu",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 96 * -1)
)

canvas.create_rectangle(
    21.0,
    105.0,
    379.0,
    106.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    88.0,
    112.0,
    312.0,
    113.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    22.0,
    180.0,
    379.0,
    264.0,
    fill="#000000",
    outline="")

canvas.create_text(
    34.0,
    230.0,
    anchor="nw",
    text="Denumeradores:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    34.0,
    185.0,
    anchor="nw",
    text="Numeradores:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    3.0,
    150.0,
    anchor="nw",
    text="Coeficientes da Função de Transferência",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    280.0,
    199.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=205.0,
    y=185.0,
    width=150.0,
    height=26.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    280.0,
    244.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=205.0,
    y=230.0,
    width=150.0,
    height=26.0
)

canvas.create_text(
    105.0,
    285.0,
    anchor="nw",
    text="Opções de Controle",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_rectangle(
    23.0,
    313.0,
    380.0,
    463.0,
    fill="#000000",
    outline="")

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    281.0,
    344.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=206.0,
    y=330.0,
    width=150.0,
    height=26.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    281.0,
    387.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=206.0,
    y=373.0,
    width=150.0,
    height=26.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    281.0,
    430.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=206.0,
    y=416.0,
    width=150.0,
    height=26.0
)

canvas.create_text(
    35.0,
    330.0,
    anchor="nw",
    text="Proporcional:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    20.0,
    416.0,
    anchor="nw",
    text="Derivativa:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    34.0,
    373.0,
    anchor="nw",
    text="Integrativa:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command= updateData,
    relief="flat"
)
button_1.place(
    x=85.0,
    y=487.0,
    width=230.0,
    height=36.0
)

entry_1.insert(0, '1')
entry_2.insert(0, '1 1')

plt.style.use('dark_background')

updateData()

window.resizable(False, False)
window.mainloop()