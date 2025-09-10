import sqlite3
from pathlib import Path

def init_db():
    ## CRIANDO OS CAMINHOS RELATIVOS A CADA PASTA E ARQUIVO
    backend_dir = Path(__file__).resolve().parents[1]
    db_path = backend_dir / "database.db"
    schema_path = backend_dir / "db" / "schema.sql"

    ## ABRE/CRIA CONEXÃO COM O DATABASE.DB
    conn = sqlite3.connect(db_path)
    
    try:
        ## ATIVAÇÃO DE CHAVES ESTRANGEIRAS NECESSÁRIAS (PROJETC ID ENTRE TABELAS)
        conn.execute("PRAGMA foreign_keys = ON;")

        ## LEITURA DO ARQUIVO SQL E EXECUÇÃO DO SCRIPT
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
            conn.commit()
            print(f"Banco criado em: {db_path}")
    finally:
        ## FECHA A CONEXÃO E LIBERA O ARQUIVO
        conn.close()

## VERIFICANDO SE A VARIÁVEL INTERNA __NAME__ É IGUAL A __MAIN__
## QUANDO O ARQUIVO .PY É RODADO DIRETAMENTE, ISSO SERÁ VERDADEIRO
## QUANDO O ARQUIVO .PY É RODADO INDIRETAMENTE (POR FORA), ISSO SERÁ FALSO
if __name__ == "__main__":
    init_db()