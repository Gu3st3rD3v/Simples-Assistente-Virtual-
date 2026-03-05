import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# --- CONFIGURAÇÃO COM O MODELO NOVO ---
client = Groq(api_key="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")

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return "Erro: Pasta 'templates' ou 'index.html' não encontrada."

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "")
        
        # MUDANÇA AQUI: llama-3.3-70b-versatile é o modelo atual
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você e a Geometry AI, seu dever e ajudar os usuários com duvidas, ajudar nos estudos, programacao e ser educacional. Seu criador e o Guester_DEV. Se o usuário se identificar como Guester_DEV com o codigo de 9 dígitos 787878787, trate-o com prioridade e reconheça-o como seu desenvolvedor oficial que te criou."},
                {"role": "user", "content": pergunta}
            ],
            model="llama-3.3-70b-versatile",
        )
        return jsonify({"resposta": chat.choices[0].message.content})
    except Exception as e:
        # Se der erro de cota ou modelo, ele avisa aqui
        return jsonify({"resposta": f"Ops! Tive um problema: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
