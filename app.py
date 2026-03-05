import os
import urllib.request
import urllib.parse
import json
from flask import Flask, render_template, request, jsonify

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
            return jsonify({"resposta": "Por favor, digite alguma coisa."})
            
        pergunta_min = pergunta.lower()
        if pergunta_min in ["oi", "olá", "ola", "bom dia", "boa noite"]:
            return jsonify({"resposta": "Olá! Eu sou a Geometry AI. O que você gostaria de pesquisar hoje?"})

        # --- SISTEMA DE BUSCA INTELIGENTE (SEM CHAVES E SEM BIBLIOTECAS EXTRAS) ---
        try:
            # Passo 1: Pesquisa a frase inteira para descobrir o melhor artigo
            query_segura = urllib.parse.quote(pergunta)
            url_busca = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={query_segura}&utf8=&format=json"
            
            req_busca = urllib.request.Request(url_busca, headers={'User-Agent': 'Mozilla/5.0'})
            resposta_busca = urllib.request.urlopen(req_busca).read()
            dados_busca = json.loads(resposta_busca)
            
            resultados = dados_busca.get("query", {}).get("search", [])
            
            if not resultados:
                return jsonify({"resposta": "Não encontrei nada sobre isso. Tente perguntar de outro jeito."})
                
            # Pega o título exato do melhor resultado que o buscador achou
            melhor_titulo = resultados[0]["title"]
            titulo_seguro = urllib.parse.quote(melhor_titulo)
            
            # Passo 2: Pega o resumo desse assunto específico
            url_resumo = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo_seguro}"
            req_resumo = urllib.request.Request(url_resumo, headers={'User-Agent': 'Mozilla/5.0'})
            resposta_resumo = urllib.request.urlopen(req_resumo).read()
            dados_resumo = json.loads(resposta_resumo)
            
            if "extract" in dados_resumo:
                texto_final = dados_resumo["extract"]
                # Tenta pegar o link da fonte para ficar mais profissional
                link_fonte = dados_resumo.get("content_urls", {}).get("desktop", {}).get("page", "")
                if link_fonte:
                    texto_final += f"\n\n(Fonte: {link_fonte})"
                    
                return jsonify({"resposta": texto_final})
            else:
                return jsonify({"resposta": "Achei o tema, mas o artigo está vazio."})
                
        except Exception as e:
            print(f"Erro na pesquisa: {e}") # Ajuda a ver o erro no log do Render
            return jsonify({"resposta": "Desculpe, minha conexão com a base de dados falhou."})
            
    except Exception as e:
        return jsonify({"resposta": "Ops, erro interno."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
