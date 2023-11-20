import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update_graph():
    # Obtenha dados do usuário (pode ser de entradas, arquivo, etc.)
    data = [1, 2, 3, 4, 5]

    # Atualize ou crie o gráfico com base nos dados
    ax.clear()
    ax.plot(data)
    
    # Atualize a exibição na interface gráfica
    canvas.draw()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gráficos Dinâmicos")

# Criação de widgets
frame = ttk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Criação de gráfico matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Incorporação do gráfico na interface Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Botão de atualização
update_button = ttk.Button(root, text="Atualizar Gráfico", command=update_graph)
update_button.pack(side=tk.BOTTOM)

# Inicie o loop principal do Tkinter
root.mainloop()
