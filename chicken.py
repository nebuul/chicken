import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import pyautogui
import time
import keyboard
import pygetwindow as gw
import webbrowser
import os
import sys

pyautogui.FAILSAFE = False

class AutoClicker:
    def __init__(self, master):
        self.master = master
        self.master.title("Auto Clique")
        self.master.geometry("500x250")
        self.master.resizable(False, False)

        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_path, 'cocorico.png')

        self.logo_image = Image.open(image_path)
        self.logo_image = self.logo_image.resize((60, 60), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.master.iconphoto(False, self.logo_photo)

        self.GRID_POINTS_X = 20
        self.GRID_POINTS_Y = 10
        self.tecla_inicio = 'F6'
        self.tecla_parada = 'F7'
        self.duracao = 10
        self.velocidade = 0.01
        self.ativo = tk.BooleanVar(value=False)
        self.config_locked = tk.BooleanVar(value=False)
        self.clique_ativo = False

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 9))
        self.style.configure('TLabel', font=('Arial', 9))
        self.style.configure('TCombobox', font=('Arial', 9))

        self.janelas_abertas = [win for win in gw.getAllTitles() if win.strip()]

        frame = ttk.Frame(master, padding="5")
        frame.pack(fill=tk.BOTH, expand=True)

        self.logo_label = ttk.Label(frame, image=self.logo_photo)
        self.logo_label.grid(row=0, column=0, rowspan=4, padx=5, pady=5)

        ttk.Label(frame, text="Selecionar Janela:").grid(row=0, column=1, sticky=tk.W, pady=2)
        self.janela_combobox = ttk.Combobox(frame, values=self.janelas_abertas, width=25)
        self.janela_combobox.grid(row=0, column=2, pady=2)

        resolucoes = ["800x600", "1024x768", "1280x720", "1366x768", "1440x900", "1600x900", "1680x1050", "1920x1080", "1920x1200", "2560x1440", "3840x2160"]

        ttk.Label(frame, text="Definir Resolução:").grid(row=1, column=1, sticky=tk.W, pady=2)
        self.resolucao_combobox = ttk.Combobox(frame, values=resolucoes, width=25)
        self.resolucao_combobox.grid(row=1, column=2, pady=2)

        ttk.Label(frame, text="Tecla para Iniciar:").grid(row=2, column=1, sticky=tk.W, pady=2)
        self.tecla_inicio_entry = ttk.Entry(frame, width=28)
        self.tecla_inicio_entry.grid(row=2, column=2, pady=2)
        self.tecla_inicio_entry.insert(0, self.tecla_inicio)
        self.tecla_inicio_entry.bind("<FocusIn>", lambda event: self.detectar_tecla(self.tecla_inicio_entry))

        ttk.Label(frame, text="Tecla para Parar:").grid(row=3, column=1, sticky=tk.W, pady=2)
        self.tecla_parada_entry = ttk.Entry(frame, width=28)
        self.tecla_parada_entry.grid(row=3, column=2, pady=2)
        self.tecla_parada_entry.insert(0, self.tecla_parada)
        self.tecla_parada_entry.bind("<FocusIn>", lambda event: self.detectar_tecla(self.tecla_parada_entry))

        ttk.Label(frame, text="Duração (segundos):").grid(row=4, column=1, sticky=tk.W, pady=2)
        self.duracao_entry = ttk.Entry(frame, width=28)
        self.duracao_entry.grid(row=4, column=2, pady=2)

        ttk.Label(frame, text="Rapidez (segundos):").grid(row=5, column=1, sticky=tk.W, pady=2)
        self.velocidade_entry = ttk.Entry(frame, width=28)
        self.velocidade_entry.grid(row=5, column=2, pady=2)
        self.velocidade_entry.insert(0, str(self.velocidade))

        self.toggle_button = tk.Button(frame, text="Desativado", command=self.toggle_program, bg="red", fg="white", font=('Arial', 9, 'bold'))
        self.toggle_button.grid(row=6, column=0, columnspan=2, pady=5, ipadx=10)

        self.lock_button = ttk.Checkbutton(frame, text="🔓 Desbloqueado", variable=self.config_locked, command=self.toggle_lock)
        self.lock_button.grid(row=6, column=2, pady=5)

        self.status_label = ttk.Label(frame, text="Inativo", foreground="red")
        self.status_label.grid(row=0, column=3, sticky='ne', padx=5)

        credit_frame = ttk.Frame(frame)
        credit_frame.grid(row=7, column=0, columnspan=3, pady=5)

        credit_label = ttk.Label(credit_frame, text="Desenvolvido por Nebul:", font=('Arial', 8), foreground="gray")
        credit_label.pack(side=tk.LEFT)

        link_label = ttk.Label(credit_frame, text="https://e-z.bio/neb.ul", font=('Arial', 8), foreground="blue", cursor="hand2")
        link_label.pack(side=tk.LEFT)
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://e-z.bio/neb.ul"))

    def toggle_lock(self):
        state = 'readonly' if self.config_locked.get() else 'normal'
        self.janela_combobox.config(state=state)
        self.resolucao_combobox.config(state=state)
        self.tecla_inicio_entry.config(state=state)
        self.tecla_parada_entry.config(state=state)
        self.duracao_entry.config(state=state)
        self.velocidade_entry.config(state=state)

        if self.config_locked.get():
            self.lock_button.config(text="🔒 Bloqueado")
        else:
            self.lock_button.config(text="🔓 Desbloqueado")

    def detectar_tecla(self, entry):
        if self.config_locked.get():
            return
        def on_press(event):
            key = event.name
            entry.delete(0, tk.END)
            entry.insert(0, key)
            keyboard.unhook_all()

        keyboard.hook(on_press)

    def toggle_program(self):
        self.ativo.set(not self.ativo.get())
        if self.ativo.get():
            self.toggle_button.config(text="Ativado", bg="green", fg="white")
            self.status_label.config(text="Ativo", foreground="green")
            threading.Thread(target=self.monitorar_teclas).start()
        else:
            self.toggle_button.config(text="Desativado", bg="red", fg="white")
            self.status_label.config(text="Inativo", foreground="red")

    def monitorar_teclas(self):
        while self.ativo.get():
            if keyboard.is_pressed(self.tecla_inicio_entry.get()) and not self.clique_ativo:
                threading.Thread(target=self.mega_clique_controlado).start()
            time.sleep(0.1)

    def obter_janela_jogo(self):
        try:
            title = self.janela_combobox.get()
            janela = gw.getWindowsWithTitle(title)[0]
            janela.activate()
            janela.restore()
            return janela._rect.left, janela._rect.top
        except Exception as e:
            print(f"Erro ao obter a janela: {e}")
            return None, None

    def mega_clique_controlado(self):
        offset_x, offset_y = self.obter_janela_jogo()
        if offset_x is None or offset_y is None:
            return

        resolucao = self.resolucao_combobox.get()
        if resolucao:
            try:
                game_width, game_height = map(int, resolucao.split('x'))
            except ValueError:
                print("Erro ao definir resolução. Usando valores padrão.")
                return

        try:
            duracao = int(self.duracao_entry.get())
        except ValueError:
            print("Erro ao definir duração. Usando valor padrão.")
            duracao = self.duracao

        try:
            velocidade = float(self.velocidade_entry.get())
        except ValueError:
            print("Erro ao definir rapidez. Usando valor padrão.")
            velocidade = self.velocidade

        passo_x = game_width // self.GRID_POINTS_X
        passo_y = game_height // self.GRID_POINTS_Y

        start_time = time.time()
        self.clique_ativo = True
        while time.time() - start_time < duracao and self.ativo.get() and self.clique_ativo:
            if keyboard.is_pressed(self.tecla_parada_entry.get()):
                self.clique_ativo = False
                break
            for i in range(self.GRID_POINTS_X):
                for j in range(self.GRID_POINTS_Y):
                    if not self.clique_ativo:
                        break
                    x = offset_x + (i * passo_x) + passo_x // 2
                    y = offset_y + (j * passo_y) + passo_y // 2
                    pyautogui.click(x, y, _pause=False)
                time.sleep(velocidade)
        self.clique_ativo = False

def main():
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()

if __name__ == "__main__":
    main()