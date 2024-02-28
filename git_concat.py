import os
import pandas as pd

# Pasta onde estão os arquivos .txt
pasta = 'C:/Users/vsfei/PIMENTA/CURSO/acelerometros_lenildo'

# Lista para armazenar os DataFrames de cada arquivo
dfs = []

# Loop pelos arquivos na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.txt') and arquivo != 'dados_concatenados.txt':
        # Extrai os 3 últimos caracteres do nome do arquivo para identificação
        identificador = arquivo[-7:-4]
        
        # Lê o arquivo em um DataFrame, ignorando a primeira linha
        df = pd.read_csv(os.path.join(pasta, arquivo), header=None, delimiter='\t', skiprows=1)
        
        # Adiciona uma coluna com o identificador do arquivo
        df['Identificador'] = identificador
        
        # Adiciona o DataFrame à lista
        dfs.append(df)

# Concatena todos os DataFrames em um único DataFrame
df_final = pd.concat(dfs, ignore_index=True)

# Renomeia as colunas do DataFrame final
df_final.columns = ['Tempo', 'Acel X', 'Acel Y', 'Acel Z', 'Local']

# Salva o DataFrame em um arquivo .txt
df_final.to_csv('dados_concatenados.txt', sep='\t', index=False)