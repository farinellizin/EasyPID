from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import control as ctl
from tkinter import messagebox, ttk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/farinellizin/Desktop/build/assets/frame0")

def stringToArray(num, den):
    numArr = num.split()
    denArr = den.split()

    numArrInt = list(map(int, numArr))
    denArrInt = list(map(int, denArr))

    return numArrInt, denArrInt

def verifyValues(num, den):
    valid_chars = set("0123456789- ")

    for element in num:
        if element not in valid_chars:
            messagebox.showerror('Input Error', 'Only numeric values, spaces, and "-" are accepted in the numerator input')
            return

    for element in den:
        if element not in valid_chars:
            messagebox.showerror('Input Error', 'Only numeric values, spaces, and "-" are accepted in the denominator input')
            return
    
    numArr, denArr = stringToArray(num, den)
    return numArr, denArr

def plotGetData(FTMF, den, control):
    if control:
        canvas.create_text(
            1000.0,
            525.0,
            anchor="nw",
            text="Gráficos com controle aplicado",
            fill="#000000",
            font=("ReadexPro Regular", 20 * -1)
        )
        y = 575
    else:
        y = 80

    time, response = ctl.step_response(FTMF)
    stepInfo = ctl.step_info(FTMF)

    time_simulation = np.arange(0, 15, 0.05, dtype=float)
    xout, yout = ctl.step_response(FTMF, time_simulation)

    omega, magnitude, phase = ctl.bode(FTMF)
    frequencyCutoffIndex = np.argmax(magnitude < -3)

    marginGain, phaseGain, _, _ = ctl.margin(FTMF) 

    # Resposta ao degrau
    figure1 = plt.figure(figsize=(4.2, 4.2), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().place(x=450, y=y)
    ax1.plot(xout, yout)

    # dPolos
    figure2 = plt.figure(figsize=(4.2, 4.2), dpi=100)
    roots, _ = ctl.root_locus(FTMF, plot=True)
    bar2 = FigureCanvasTkAgg(plt.gcf(), window)
    bar2.get_tk_widget().place(x=950, y=y)

    # Bode
    figure3 = plt.figure(figsize=(4.2, 4.2), dpi=100)
    ax3 = figure3.add_subplot(111)
    frequency = np.logspace(-1, 2, 100)
    _, mag, phase = ctl.bode_plot(FTMF, omega=frequency, dB=True, plot=True)
    ax3.semilogx(frequency, mag)
    bar3 = FigureCanvasTkAgg(figure3, window)
    bar3.get_tk_widget().place(x=1450, y=y)

    roots = np.roots(den)

    maxPeakValue = np.max(response)

    # Instante de Pico
    peakTime = stepInfo['PeakTime']

    # Tempo de estabilização
    settlingTime = stepInfo['SettlingTime']

    # Ultrapassagem percentual
    overshootPercentage = stepInfo['Overshoot']

    # Valor final
    finalValue = stepInfo['SteadyStateValue']

    # Frequência de Corte
    frequencyCutoff = omega[frequencyCutoffIndex]

    # Ganho em dB
    dBGain = ctl.mag2db(np.abs(magnitude))
    dBGain = dBGain[0]

    # Ganho estático
    staticGain = 10 ** (dBGain / 20)

    return roots, maxPeakValue, peakTime, settlingTime, overshootPercentage, finalValue, frequencyCutoff, marginGain, phaseGain, dBGain, staticGain

def updateData():
    if not entry_3.get() and entry_4.get() and entry_5.get():
        messagebox.showerror('PID Error', 'The combination integrative-derivative is not supported')
        return

    numeratorEntry = entry_1.get()
    denominatorEntry = entry_2.get()
    
    rootsControl = ''
    maxPeakValueControl = ''
    peakTimeControl = ''
    settlingTimeControl = ''
    overshootPercentageControl = ''
    finalValueControl = ''

    num, den = verifyValues(numeratorEntry, denominatorEntry)

    if len(num) > len(den):
        messagebox.showerror('Data Error', 'There`s no such system with more zeros than poles')
        return

    system = ctl.TransferFunction(num, den)
    FTMF = ctl.minreal(system / (1 + system))

    if entry_3.get() and not entry_4.get() and not entry_5.get(): # proporcional
        K = int(entry_3.get())
        FTMFP = ctl.minreal((K * system) / (1 + (K * system)))
        rootsControl, maxPeakValueControl, peakTimeControl, settlingTimeControl, overshootPercentageControl, finalValueControl, frequencyCutoffControl, marginGainControl, phaseGainControl, dBGainControl, staticGainControl = plotGetData(FTMFP, den, True)
        
    elif not entry_3.get() and entry_4.get() and not entry_5.get(): # integrativa
        Ki = int(entry_4.get())
        integralController = ctl.TransferFunction(Ki, [1, 0])
        FTMFI = ctl.minreal((integralController * system) / (1 + (integralController * system)))
        rootsControl, maxPeakValueControl, peakTimeControl, settlingTimeControl, overshootPercentageControl, finalValueControl, frequencyCutoffControl, marginGainControl, phaseGainControl, dBGainControl, staticGainControl = plotGetData(FTMFI, den, True)

    elif not entry_3.get() and not entry_4.get() and entry_5.get(): # derivativa
        Kd = int(entry_5.get())
        derivativeController = ctl.TransferFunction([Kd, 0], [1]) # ? perguntar thabatta
        FTMFD = ctl.minreal((derivativeController * system) / (1 + (derivativeController * system)))
        rootsControl, maxPeakValueControl, peakTimeControl, settlingTimeControl, overshootPercentageControl, finalValueControl, frequencyCutoffControl, marginGainControl, phaseGainControl, dBGainControl, staticGainControl = plotGetData(FTMFD, den, True)

    elif entry_3.get() and entry_4.get() and not entry_5.get(): # proporcional - integrativa
        K = int(entry_3.get())
        Ki = int(entry_4.get())
        PIController = ctl.TransferFunction([K, Ki], [1, 0])
        FTMFPI = ctl.minreal((PIController * system) / (1 + (PIController * system)))
        rootsControl, maxPeakValueControl, peakTimeControl, settlingTimeControl, overshootPercentageControl, finalValueControl, frequencyCutoffControl, marginGainControl, phaseGainControl, dBGainControl, staticGainControl = plotGetData(FTMFPI, den, True)

    elif entry_3.get() and not entry_4.get() and entry_5.get(): # proporcional - derivativa
        K = int(entry_3.get())
        Kd = int(entry_5.get())
        PDController = ctl.TransferFunction([K, Kd], [1])
        FTMFPD = ctl.minreal((PDController * system) / (1 + (PDController * system)))
        rootsControl, maxPeakValueControl, peakTimeControl, settlingTimeControl, overshootPercentageControl, finalValueControl, frequencyCutoffControl, marginGainControl, phaseGainControl, dBGainControl, staticGainControl = plotGetData(FTMFPD, den, True)

    elif entry_3.get() and entry_4.get() and entry_5.get(): # proporcional - integrativa - derivativa
        K = int(entry_3.get())
        Ki = int(entry_4.get())
        Kd = int(entry_5.get())
        PIDController = ctl.TransferFunction([Kd, K, Ki], [1, 0])
        FTMFPID = ctl.minreal((PIDController * system) / (1 + (PIDController * system)))
        rootsControl, maxPeakValueControl, peakTimeControl, settlingTimeControl, overshootPercentageControl, finalValueControl, frequencyCutoffControl, marginGainControl, phaseGainControl, dBGainControl, staticGainControl = plotGetData(FTMFPID, den, True)

    roots, maxPeakValue, peakTime, settlingTime, overshootPercentage, finalValue, frequencyCutoff, marginGain, phaseGain, dBGain, staticGain = plotGetData(FTMF, den, False)

    if entry_3.get() or entry_4.get() or entry_5.get():
        dados_tabela = [
            ("Raízes", roots, rootsControl),
            ("Valor de Pico", f'{maxPeakValue:.3f}', f'{maxPeakValueControl:.3f}'),
            ("Pico (t)", f'{peakTime:.3f}', f'{peakTimeControl:.3f}'),
            ("Estabilização (t)", f'{settlingTime:.3f}', f'{settlingTimeControl:.3f}'),
            ("Overshoot (%)", f'{overshootPercentage:.3f}', f'{overshootPercentageControl:.3f}'),
            ("Valor final", f'{finalValue:.3f}', f'{finalValueControl:.3f}'),
            ("Freq. Corte (Rad/s)", f'{frequencyCutoff:.3f}', f'{frequencyCutoffControl:.3f}'),
            ("Margem de Ganho", f'{marginGain:.3f}', f'{marginGainControl:.3f}'),
            ("Margem de Fase", f'{phaseGain:.3f}', f'{phaseGainControl:.3f}'),
            ("Ganho (dB)", f'{dBGain:.3f}', f'{dBGainControl:.3f}'),
            ("Ganho Estático", f'{staticGain:.3f}', f'{staticGainControl:.3f}')
        ]
    else:
        dados_tabela = [
            ("Raízes", roots, '[]'),
            ("Valor de Pico", f'{maxPeakValue:.3f}', 0),
            ("Pico (t)", f'{peakTime:.3f}', 0),
            ("Estabilização (t)", f'{settlingTime:.3f}', 0),
            ("Overshoot (%)", f'{overshootPercentage:.3f}', 0),
            ("Valor final", f'{finalValue:.3f}', 0),
            ("Freq. Corte (Rad/s)", f'{frequencyCutoff:.3f}', 0),
            ("Margem de Ganho", f'{marginGain:.3f}', 0),
            ("Margem de Fase", f'{phaseGain:.3f}', 0),
            ("Ganho (dB)", f'{dBGain:.3f}', 0),
            ("Ganho Estático", f'{staticGain:.3f}', 0)
        ]

    style = ttk.Style()
    style.configure("Treeview", background='black', foreground="white")

    table = ttk.Treeview(window, height=11, style="Treeview")
    table['columns'] = ('', 'Sem controle', 'Com controle')
    table.column('#0', width=0, stretch=False)
    table.column('', anchor="center", width=140)
    table.column('Sem controle', anchor="center", width=120)
    table.column('Com controle', anchor="center", width=120)

    table.heading('#0', text='', anchor="center")
    table.heading('', text='', anchor="center")
    table.heading('Sem controle', text='Sem controle', anchor="center")
    table.heading('Com controle', text='Com controle', anchor="center")

    for i, (rotulo_linha, valor_coluna1, valor_coluna2) in enumerate(dados_tabela, start=0):
        table.insert(parent='', index=i, iid=i, text='', values=(rotulo_linha, valor_coluna1, valor_coluna2))

    table.place(x=8, y=550)
    

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
    28.0,
    230.0,
    anchor="nw",
    text="Denumeradores:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    28.0,
    185.0,
    anchor="nw",
    text="Numeradores:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    105.0,
    150.0,
    anchor="nw",
    text="Coeficientes da FT",
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
    28.0,
    330.0,
    anchor="nw",
    text="Proporcional:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    28.0,
    416.0,
    anchor="nw",
    text="Derivativa:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    28,
    373.0,
    anchor="nw",
    text="Integrativa:",
    fill="#FFFFFF",
    font=("ReadexPro Regular", 20 * -1)
)

canvas.create_text(
    1000.0,
    30.0,
    anchor="nw",
    text="Gráficos sem controle aplicado",
    fill="#000000",
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