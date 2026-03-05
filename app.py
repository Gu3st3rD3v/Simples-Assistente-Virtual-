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
            return jsonify({"resposta": "Por favor, digite algo."})

        # Sistema de pesquisa DuckDuckGo
        try:
            with DDGS() as ddgs:
                # Busca o resultado mais relevante
                resultados = list(ddgs.text(pergunta, region='br-pt', max_results=1))
                if resultados:
                    resumo = resultados[0]['body']
                    link = resultados[0]['href']
                    return jsonify({"resposta": f"{resumo}\n\nFonte: {link}"})
        except Exception:
            pass

        # Se o buscador falhar, tenta o Wikipedia como segunda opção
        try:
            import urllib.request, json, urllib.parse
            termo = urllib.parse.quote(pergunta)
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())
                return jsonify({"resposta": data.get("extract", "Não encontrei informações exatas.")})
        except Exception:
            return jsonify({"resposta": "Desculpe, não consegui encontrar uma resposta agora."})

    except Exception as e:
        return jsonify({"resposta": "Erro interno no servidor."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
