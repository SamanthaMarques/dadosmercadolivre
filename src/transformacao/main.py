import pandas as pd
import sqlite3
from datetime import datetime

jsonl_path = '../data/data.jsonl'

# Lê o arquivo JSONL e cria um DataFrame
df = pd.read_json('..\data\data.jsonl', lines=True)

# Exibe todas as colunas no Pandas
pd.options.display.max_columns = None

# Adiciona a fonte dos dados e a data da coleta
df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-feminino"

df['_data_coleta'] = datetime.now()

# Substitui valores nulos por 0 e converte para tipo numérico
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Limpa a coluna de avaliações e converte para inteiro
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Calcula o preço total (reais + centavos)
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remove as colunas separadas de preço
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'])

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('../data/quotes.db')

# Salva os dados no banco de dados
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fecha a conexão com o banco
conn.close()

# Exibe as primeiras linhas dos dados
print(df.head())