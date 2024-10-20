import pandas as pd
import glob
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Dizionario che associa il nome del mese al numero
mesi_numeri = {
    "GEN": "01", "FEB": "02", "MAR": "03", "APR": "04",
    "MAG": "05", "GIU": "06", "LUG": "07", "AGO": "08",
    "SET": "09", "OTT": "10", "NOV": "11", "DIC": "12"
}

# Variabili globali per memorizzare il mese e l'anno selezionato
mese_selezionato = None
numero_mese = None
anno_selezionato = None

# Funzione per aggiornare il file CSV
def aggiorna_csv():
    # Trova tutti i file CSV nella cartella
    file_paths = glob.glob("strao_files/*.csv")

    # Se non ci sono file CSV nella cartella, mostra un errore
    if not file_paths:
        messagebox.showerror("Errore", "Nessun file CSV trovato nella cartella 'strao_files'.")
        return

    # Leggi ogni file CSV in un DataFrame e memorizzali in una lista
    dataframes = [pd.read_csv(file, sep=";") for file in file_paths]

    # Concatena tutti i DataFrame in un unico DataFrame
    df_concatenato = pd.concat(dataframes, ignore_index=True)

    # Modifica i dati del DataFrame
    df_concatenato['Evento'] = 'PROV'
    df_concatenato.insert(2, 'Anno', anno_selezionato)
    df_concatenato.insert(3, 'Mese', numero_mese)
    df_concatenato.insert(4, 'Mese2', mese_selezionato)
    df_concatenato['Ambiente'] = '*'
    df_concatenato['Raggruppamento'] = ''
    df_concatenato['Decodifica di Raggruppamento'] = ''
    df_concatenato['Codice Paghe'] = 'D'
    df_concatenato = df_concatenato.replace({'Straordinario NOF': 'STR.NOF', 'Straordinario NEF': 'STR.NEF', 'Straordinario DIU': 'STR.DIU'})

    df_concatenato.insert(12, 'Nr_Det', "284")
    df_concatenato.insert(13, 'Tipo', "STR")

    # Reindex delle colonne per ordine desiderato
    df_concatenato = df_concatenato.reindex(columns=[
        "Evento", "Data Inizio", "Matricola", "Anno", "Mese", "Mese2",
        "Desc. Voce TE", "Ambiente", "Raggruppamento", "Valore",
        "Decodifica di Raggruppamento", "Codice Paghe", "Anno", "Nr_Det", "Tipo"
    ])

    # Salva il DataFrame aggiornato in un file CSV
    output_file = 'voci_paga_strao.csv'
    try:
        df_concatenato.to_csv(output_file, sep=';', header=False, index=False)
        messagebox.showinfo("Successo", f"I dati sono stati salvati correttamente nel file '{output_file}'")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il salvataggio del file CSV: {e}")

# Funzione che viene chiamata quando il pulsante viene cliccato
def salva_dati():
    global mese_selezionato, numero_mese, anno_selezionato
    mese_selezionato = combo_mesi.get()  # Prendi il mese selezionato dalla Combobox
    anno_selezionato = combo_anni.get()  # Prendi l'anno selezionato dalla Combobox
    if mese_selezionato and anno_selezionato:
        numero_mese = mesi_numeri[mese_selezionato]  # Ottieni il numero del mese
        
        # Mostra un messaggio con i dati selezionati
        messagebox.showinfo("Dati salvati", f"Mese: {mese_selezionato} (Numero: {numero_mese}), Anno: {anno_selezionato}")
        
        # Aggiorna il CSV con i nuovi dati
        aggiorna_csv()

        print(f"Mese selezionato: {mese_selezionato} (Numero: {numero_mese}), Anno selezionato: {anno_selezionato}")
    else:
        messagebox.showerror("Errore", "Seleziona un mese e un anno validi")

# Crea la finestra principale
root = tk.Tk()
root.title("Selezione del Mese e Anno")

# Definisci l'elenco dei mesi
mesi = list(mesi_numeri.keys())

# Definisci l'elenco degli anni (puoi personalizzare la lista)
anni = [str(anno) for anno in range(2000, 2031)]  # Anni dal 2000 al 2030

# Crea un'etichetta per la ComboBox del mese
label_mese = tk.Label(root, text="Seleziona un mese:")
label_mese.grid(row=0, column=0, padx=10, pady=10)

# Crea una ComboBox per la selezione dei mesi
combo_mesi = ttk.Combobox(root, values=mesi, state="readonly")
combo_mesi.grid(row=0, column=1, padx=10, pady=10)
combo_mesi.set("GEN")  # Imposta un valore predefinito

# Crea un'etichetta per la ComboBox dell'anno
label_anno = tk.Label(root, text="Seleziona un anno:")
label_anno.grid(row=1, column=0, padx=10, pady=10)

# Crea una ComboBox per la selezione degli anni
combo_anni = ttk.Combobox(root, values=anni, state="readonly")
combo_anni.grid(row=1, column=1, padx=10, pady=10)
combo_anni.set("2024")  # Imposta un valore predefinito

# Crea il pulsante per salvare i dati
btn_salva = tk.Button(root, text="Salva", command=salva_dati)
btn_salva.grid(row=2, columnspan=2, pady=10)

# Avvia il loop della finestra
root.mainloop()
