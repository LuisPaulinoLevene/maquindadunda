from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou configure com os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html") as file:
        return file.read()

class NumeroInput(BaseModel):
    numero: str

def aplicar_formula(numero: str) -> str:
    soma = [int(numero[i]) + int(numero[i + 1]) for i in range(0, 13, 2)]
    soma = [x % 10 if x >= 10 else x for x in soma]
    resultado = ''.join(map(str, soma)) + numero[0]
    return resultado

@app.post("/calcular/")
async def calcular_numero(numero_input: NumeroInput):
    numero = numero_input.numero
    if len(numero) != 15 or not numero.isdigit():
        return {"error": "O número deve ter 15 dígitos."}

    resultado = aplicar_formula(numero)
    return {"resultado": resultado}