import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Coloque sua API Key aqui dentro das aspas
genai.configure(api_key="SUA_CHAVE_AQUI")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "")
        
        if not pergunta:
            return jsonify({"resposta": "Você enviou uma mensagem vazia."})

        resposta_ia = model.generate_content(pergunta)
        return jsonify({"resposta": resposta_ia.text})
    except Exception as e:
        return jsonify({"resposta": f"Erro na IA: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
