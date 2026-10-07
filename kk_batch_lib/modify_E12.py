import sys

def remove_lines(filename, num_lines):
    # Leggi tutte le righe tranne le prime num_lines
    with open(filename, 'r') as file:
        lines = file.readlines()[num_lines:]

    # Sovrascrivi il file con le righe rimanenti
    with open(filename, 'w') as file:
        file.writelines(lines)

# Controllo se è stato passato correttamente il nome del file come argomento
if len(sys.argv) != 2:
    print("Usage: python script.py input_file.txt")
    sys.exit(1)

input_file = sys.argv[1]

remove_lines(input_file, 5)

# Apro il file di input e leggo le righe
with open(input_file, 'r') as f:
    lines = f.readlines()

# Apro il file di output in modalità scrittura
output_file = input_file
with open(output_file, 'w') as f:
    for line in lines:
        # Divido la riga in base agli spazi e converto i valori in float
        numbers = line.strip().split()
        numbers = [float(num) for num in numbers]

        # Se la lunghezza del numero è minore di 7 caratteri, aggiungo uno spazio dopo il primo numero
        if len(str(numbers[0])) < 7:
            f.write(' '.join([f"{num}" for num in numbers]) + '\n')
        else:
            f.write(' '.join([f"{num}" for num in numbers]) + '\n')
