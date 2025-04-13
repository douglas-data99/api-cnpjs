from fastapi import FastAPI, Query
import pandas as pd
import duckdb

app = FastAPI()
db = duckdb.connect(database=':memory:')

# Carrega o Parquet na memória
df = pd.read_parquet("BaseCNPJ.parquet")
db.register("base", df)

@app.get("/dados")
def get_dados(
    uf: str = Query(None),
    ddd: str = Query(None),
    lote: int = Query(None)
):
    query = "SELECT * FROM base WHERE 1=1"
    if uf:
        query += f" AND UF = '{uf}'"
    if ddd:
        query += f" AND DDD1 = '{ddd}'"
    if lote:
        query += f" AND Lote = {lote}"
    result = db.execute(query).df()
    return result.to_dict(orient="records")
