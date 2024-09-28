import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = ""
SUPABASE_KEY = ""

# Função para conectar ao Supabase
def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para buscar dados da tabela
def fetch_data_from_supabase():
    supabase = get_supabase_client()
    response = supabase.table("carlinha").select("*").execute()
    return response.data

# Aplicativo Streamlit
def main():
    st.title("Visualização de Dados do Supabase")
    st.subheader("Dados da tabela 'carlinha'")

    # Fetching data
    data = fetch_data_from_supabase()

    if data:
        # Processando os dados para exibição
        processed_data = []
        for row in data:
            # Se 'data_linha' já for um dicionário, podemos usá-lo diretamente
            if isinstance(row['data_linha'], dict):
                row['data_linha'] = row['data_linha']  # já está em formato de dicionário
            processed_data.append(row)

        df = pd.DataFrame(processed_data)
        st.write("Dados encontrados:")

        # Exibir dataframe
        st.dataframe(df)

        # Opcional: Exibir um gráfico simples, se necessário
        if st.checkbox("Mostrar Gráfico de Dados"):
            for column in df['data_linha'].iloc[0].keys():
                # Criar uma lista de valores para o gráfico
                values = [d['data_linha'][column] for d in processed_data]
                st.line_chart(values)  # Removido o argumento 'name'

    else:
        st.write("Nenhum dado encontrado.")

if __name__ == "__main__":
    main()
