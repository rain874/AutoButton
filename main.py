# -*- coding: utf-8 -*-
import tkinter as tk
import configparser

import pyautogui
import time
import keyboard


class AutoButtonApp:
    def __init__(self, master, config_datei):
        self.master = master
        self.master.title("AutoButton - by Rainer Schmitz")
        self.config = self.lade_konfiguration(config_datei)
        self.erzeuge_widgets()
        self.passe_fenster_an()  # Fenstergröße nach dem Erzeugen der Widgets anpassen

    def lade_konfiguration(self, dateipfad):
        config = configparser.ConfigParser()
        with open(dateipfad, "r", encoding="utf-8") as datei:
            config.read_file(datei)
        return config

    def erzeuge_widgets(self):
        # Abstandseinstellungen (extern und intern)
        button_padx = 2   # horizontaler Abstand zwischen den Buttons
        button_pady = 2   # vertikaler Abstand zwischen den Buttons
        button_ipadx = 2  # horizontaler innerer Abstand (Padding im Button)
        button_ipady = 2  # vertikaler innerer Abstand (Padding im Button)

        # Checkbox für "Immer im Vordergrund"
        self.var_topmost = tk.BooleanVar()
        self.check_topmost = tk.Checkbutton(
            self.master,
            text="Immer im Vordergrund",
            variable=self.var_topmost,
            command=self.toggle_topmost,
            font=("Arial", 10)
        )
        self.check_topmost.grid(row=0, column=0, padx=button_padx, pady=button_pady, sticky='w')

        buttons_pro_spalte = 20  # Anzahl der Buttons pro Spalte

        for index, section in enumerate(self.config.sections()):
            # Lese den Bool-Wert "enabled" aus der Konfiguration (Standard: True)
            enabled = self.config.getboolean(section, 'enabled', fallback=True)
            if not enabled:
                continue  # Button wird nicht erstellt, wenn enabled False ist

            text = self.config.get(section, 'text',fallback='Button')
            color = self.config.get(section, 'color', fallback='white')
            betreff = self.config.get(section, 'betreff', fallback='')
            beschreibung = self.config.get(section, 'beschreibung', fallback='')


            def button_callback(b=betreff, bs=beschreibung):
                self.simuliere_tastatureingaben(b, bs)

            button = tk.Button(
                self.master,
                text=text,
                bg=color,
                command=button_callback
            )


            # Berechne die aktuelle Zeile und Spalte basierend auf dem Index
            current_row = (index % buttons_pro_spalte) + 1  # +1 wegen der Checkbox in Zeile 0
            current_column = index // buttons_pro_spalte

            button.grid(
                row=current_row,
                column=current_column,
                padx=button_padx,
                pady=button_pady,
                sticky='w',
                ipadx=button_ipadx,
                ipady=button_ipady
            )

    def toggle_topmost(self):
        self.master.attributes('-topmost', self.var_topmost.get())

    def simuliere_tastatureingaben(self, betreff, beschreibung):
        time.sleep(2)  # Wartezeit, um sicherzustellen, dass das richtige Fenster den Fokus hat

        # 3-mal Tab
        for _ in range(3):
            pyautogui.press('tab')

        # Betreff einfügen
        keyboard.write(betreff)

        # 6-mal Tab
        for _ in range(6):
            pyautogui.press('tab')

        # Richtung auf "eingehende" setzen
        pyautogui.typewrite('eingehende')

        # 2-mal Pfeiltaste hoch
        for _ in range(2):
            pyautogui.press('up')

        # Enter
        pyautogui.press('enter')

        # 2-mal Tab
        for _ in range(2):
            pyautogui.press('tab')

        # Schreiben des Textes
        keyboard.write(beschreibung)

    def passe_fenster_an(self):
        # Erzwinge, dass alle Widget-Größen berechnet werden
        self.master.update_idletasks()
        # Ermittel die benötigte Breite und Höhe
        breite = self.master.winfo_reqwidth()
        hoehe = self.master.winfo_reqheight()
        # Setze die Fenstergröße basierend auf den abgerufenen Werten
        self.master.geometry(f"{breite}x{hoehe}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoButtonApp(root, 'konfiguration.ini')
    root.mainloop()

