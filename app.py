import os
from flask import Flask, render_template, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "").strip()
        
        if not pergunta:
            return jsonify({"resposta": "Por favor, digite sua pergunta ou código."})

        # --- MOTOR DE INTELIGÊNCIA GEOMETRY AI (SEM CHAVE) ---
        try:
            with DDGS() as ddgs:
                # O comando .chat() acessa a IA de verdade que sabe programar!
                # Usamos o modelo 'gpt-4o-mini' que é excelente para scripts.
                resposta_ia = ddgs.chat(pergunta, model='gpt-4o-mini')
                
                if resposta_ia:
                    return jsonify({"resposta": resposta_ia})
        except Exception as e:
            print(f"Erro no modo Chat: {e}")
            
        # Fallback: Se o modo chat falhar, ele tenta a busca normal
        try:
            with DDGS() as ddgs:
                res = list(ddgs.text(pergunta, region='br-pt', max_results=1))
                if res:
                    return jsonify({"resposta": res[0]['body']})
        except:
            return jsonify({"resposta": "No momento não consegui processar sua solicitação."})

    except Exception:
        return jsonify({"resposta": "Erro interno no servidor da Geometry AI."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
