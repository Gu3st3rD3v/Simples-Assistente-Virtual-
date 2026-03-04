import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# CONFIGURAÇÃO DA IA (Coloque sua chave aqui ou no Render)
GOOGLE_API_KEY = "SUA_CHAVE_AQUI"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta_usuario = dados.get("pergunta", "")

        if not pergunta_usuario:
            return jsonify({"resposta": "Você não digitou nada..."})

        # A IA processa a pergunta e gera a resposta baseada na internet
        response = model.generate_content(pergunta_usuario)
        
        return jsonify({"resposta": response.text})
    except Exception as e:
        return jsonify({"resposta": f"Erro na IA: {str(e)}"})

if __name__ == '__main__':
    # O Render exige que o host seja 0.0.0.0 e a porta venha da variável de ambiente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
