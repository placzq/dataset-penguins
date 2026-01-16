import seaborn as sns 
import matplotlib.pyplot as plt 
import tkinter as tk 


tabelka = sns.load_dataset("penguins")


print("Pierwsze wiersze:")
print(tabelka.head()) 

print("\nInfo o danych:")
tabelka.info() 

print("\nStatystyki:")
print(tabelka.describe()) 

print("\nBraki danych:")
print(tabelka.isnull().sum()) 

# uzzupełnianie braków 
for kolumna in ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]:
    tabelka[kolumna] = tabelka[kolumna].fillna(tabelka[kolumna].mean())


print("\nBraki danych po uzupełnieniu:")
print(tabelka.isnull().sum())

najczestsza_plec = tabelka["sex"].mode()[0]   
tabelka["sex"] = tabelka["sex"].fillna(najczestsza_plec) 


print("\nBraki danych po uzupełnieniu kolumny 'sex':")
print(tabelka.isnull().sum())



# histogram rozkładu masy ciała pingwinów
def wykres_histogram():
    plt.figure()
    sns.histplot(tabelka["body_mass_g"])
    plt.title("Rozkład masy ciała pingwinów")
    plt.xlabel("Masa ciała (g)")
    plt.ylabel("Liczba pingwinów")
    plt.show()

# porownanie masy między gatunkami (słupki)
def wykres_srednia_gatunki():
    plt.figure()
    sns.barplot(data=tabelka, x="species", y="body_mass_g")
    plt.title("Średnia masa ciała dla każdego gatunku")
    plt.xlabel("Gatunek")
    plt.ylabel("Masa ciała (g)")
    plt.show()

#zależność między cechami, pletwa a masa ciala
def wykres_scatter():
    plt.figure()
    sns.scatterplot(data=tabelka, x="flipper_length_mm", y="body_mass_g", hue="species")
    plt.title("Zależność: długość płetwy vs masa ciała")
    plt.xlabel("Długość płetwy (mm)")
    plt.ylabel("Masa ciała (g)")
    plt.show()

#wartosci odstajace
def wykres_outliery():
    plt.figure()
    sns.boxplot(data=tabelka, x="species", y="body_mass_g")
    plt.title("Analiza outlierów: masa ciała wg gatunku")
    plt.xlabel("Gatunek")
    plt.ylabel("Masa ciała (g)")
    plt.show()

#korelacje cech
def wykres_korelacje():
    dane_numeryczne = tabelka.select_dtypes(include="number")
    macierz_korelacji = dane_numeryczne.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(macierz_korelacji, annot=True, cmap="coolwarm")
    plt.title("Macierz korelacji cech numerycznych pingwinów")
    plt.show()

#gui
root = tk.Tk()
root.title("Analiza datasetu Penguins - menu wykresów, Patrycja Łączka")
root.geometry("900x633")
root.resizable(False, False)

canvas = tk.Canvas(root, width=900, height=633, highlightthickness=0)
canvas.pack(fill="both", expand=True)


bg_img = tk.PhotoImage(file="tlo.png")
panel_img = tk.PhotoImage(file="panel.png")


canvas.create_image(0, 0, anchor="nw", image=bg_img)

panel_x = 900 - 360   
panel_y = 40          
canvas.create_image(panel_x, panel_y, anchor="nw", image=panel_img)


canvas.create_text(
    panel_x + 160, panel_y + 35,
    text="Wybierz wykres:",
    font=("Segoe UI", 16, "bold"),
    fill="#003344"
)

def aero_button(text, cmd, x, y):
    btn = tk.Button(
        root,
        text=text,
        command=cmd,
        font=("Segoe UI", 11, "bold"),
        bg="#c9f2ff",           # jaśniejsze “aero”
        fg="#003344",
        activebackground="#e8fbff",
        activeforeground="#003344",
        relief="groove",        # daje delikatną ramkę 3D
        bd=2,
        padx=12,
        pady=10,
        highlightthickness=1,
        highlightbackground="#ffffff"
    )


    def on_enter(e): btn.config(bg="#e8fbff")
    def on_leave(e): btn.config(bg="#c9f2ff")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    canvas.create_window(x, y, anchor="nw", window=btn, width=280)



start_x = panel_x + 20
start_y = panel_y + 70
gap = 55

aero_button("Wykres I: Rozkład masy (histogram)", wykres_histogram, start_x, start_y + gap*0)
aero_button("Wykres II: Średnia masa wg gatunku", wykres_srednia_gatunki, start_x, start_y + gap*1)
aero_button("Analiza zależności: Płetwa vs masa", wykres_scatter, start_x, start_y + gap*2)
aero_button("Outliery (wartości odstające)", wykres_outliery, start_x, start_y + gap*3)
aero_button("Korelacje (heatmapa)", wykres_korelacje, start_x, start_y + gap*4)

aero_button("Zamknij", root.destroy, start_x, start_y + gap*6)

root.mainloop()
