import pandas as pd
import json
import datetime
from supabase import create_client, Client
from io import StringIO  # Importa StringIO do módulo correto

# Configurações do Supabase
SUPABASE_URL = ""
SUPABASE_KEY = ""
BUCKET_NAME = "carla"


# Função para conectar ao Supabase
def get_supabase_client() -> Client:
  return create_client(SUPABASE_URL, SUPABASE_KEY)


# Função para ler CSV do bucket do Supabase e transformar os dados
def process_csv_from_bucket(supabase: Client, bucket_name: str,
                            file_name: str):
  # Baixa o arquivo CSV do bucket
  response = supabase.storage.from_(bucket_name).download(file_name)
  print(response)

  if response is None:
    print(f"Erro ao baixar o arquivo: {file_name}")
    return

  # Decodifica o conteúdo do arquivo CSV (o response é um objeto de bytes)
  csv_data = response.decode('utf-8')

  # Usa StringIO do módulo io para tratar a string como arquivo
  df = pd.read_csv(StringIO(csv_data))

  # Processa cada linha e faz o insert no Supabase
  for index, row in df.iterrows():
    data_line = row.to_json()
    data_ingestao = datetime.datetime.utcnow().isoformat()

    # Criação do objeto de dados a ser inserido
    data = {"data_ingestao": data_ingestao, "data_linha": json.loads(data_line)}

    # Faz o insert no Supabase
    supabase.table("carlinha").insert(data).execute()


    # Exemplo de uso
if __name__ == "__main__":
  supabase_client = get_supabase_client()
  file_name = "wine.data"
  process_csv_from_bucket(supabase_client, BUCKET_NAME, file_name)
