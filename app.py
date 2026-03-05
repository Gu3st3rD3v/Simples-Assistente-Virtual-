import os
from groq import Groq
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)
timezone = pytz.timezone('America/Sao_Paulo')

# --- CONFIGURAÇÃO ---
# Coloque sua Key entre as aspas abaixo
client = Groq(api_key="SUA_CHAVE_AQUI")

COMANDOS_FIXOS = {
    "quem é você": "Eu sou a Geometry AI, sua assistente focada em tecnologia.",
    "quem te criou": "Fui desenvolvida pelo Guester_DEV.",
    "bom dia": "Bom dia! Como posso ajudar hoje?"
}

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json
    pergunta_original = dados.get("pergunta", "").strip()
    msg = pergunta_original.lower()

    if not msg:
        return jsonify({"resposta": "Diga algo!"})

    # 1. DATA E HORA
    agora = datetime.now(timezone)
    if "horas" in msg:
        return jsonify({"resposta": f"Agora são {agora.strftime('%H:%M')}."})
    
    # 2. COMANDOS FIXOS
    if msg in COMANDOS_FIXOS:
        return jsonify({"resposta": COMANDOS_FIXOS[msg]})

    # 3. INTELIGÊNCIA ARTIFICIAL (GROQ)
    try:
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é a Geometry AI. Responda curto."},
                {"role": "user", "content": pergunta_original}
            ],
            model="llama3-8b-8192",
        )
        return jsonify({"resposta": chat.choices[0].message.content})
    except Exception as e:
        return jsonify({"resposta": "Erro na conexão com a IA."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
