import os
from groq import Groq
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- CONFIGURAÇÃO COM SUA CHAVE ---
CHAVE = "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" 

try:
    client = Groq(api_key=CHAVE)
except Exception as e:
    client = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json
    pergunta = dados.get("pergunta", "").strip()

    if not pergunta:
        return jsonify({"resposta": "Diga algo!"})

    try:
        # Usando o modelo Llama 3.3 que é muito estável
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é a Geometry AI, uma assistente prestativa. Responda sempre em português brasileiro de forma clara."},
                {"role": "user", "content": pergunta}
            ],
            model="llama-3.3-70b-versatile",
        )
        return jsonify({"resposta": chat.choices[0].message.content})
    except Exception as e:
        # Se der erro, ele vai te mostrar o motivo real no chat
        return jsonify({"resposta": f"Erro na conexão com a Groq: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
