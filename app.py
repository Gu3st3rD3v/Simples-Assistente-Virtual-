import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURAÇÃO DA IA ---
# Substitua pelo código da sua chave ou configure no painel do Render
GOOGLE_API_KEY = "COLE_AQUI_SUA_CHAVE_DO_AI_STUDIO"
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
            return jsonify({"resposta": "Diga algo para eu pesquisar!"})

        # A IA pesquisa na base de dados dela (treinada com a internet)
        response = model.generate_content(pergunta_usuario)
        
        return jsonify({"resposta": response.text})
    except Exception as e:
        return jsonify({"resposta": f"Erro ao processar: {str(e)}"})

if __name__ == '__main__':
    # ESSA PARTE É ESSENCIAL PARA O RENDER FUNCIONAR:
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
