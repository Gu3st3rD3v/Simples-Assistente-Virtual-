import os
from flask import Flask, render_template, request, jsonify, session
from duckduckgo_search import DDGS
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)
timezone = pytz.timezone('America/Sao_Paulo')

# --- BANCO DE DADOS DO AKINATOR ---
PERGUNTAS_AKINATOR = {
    1: "O seu personagem é um ser humano real?",
    2: "Ele é um super-herói?",
    3: "Ele é brasileiro?",
    4: "Ele é de um anime?",
    5: "Ele usa uma armadura?"
}

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta_original = dados.get("pergunta", "").strip()
        pergunta = pergunta_original.lower()
        
        # --- LÓGICA AKINATOR ---
        if "akinator" in pergunta:
            session['jogo'] = 'akinator'
            session['passo'] = 1
            return jsonify({"resposta": "🔮 Akinator invocado! Pense em um personagem famoso. Quando estiver pronto, diga 'ESTOU PRONTO'."})

        if session.get('jogo') == 'akinator':
            passo = session.get('passo')
            if "pronto" in pergunta and passo == 1:
                session['passo'] = 2
                return jsonify({"resposta": PERGUNTAS_AKINATOR[1]})
            if passo >= 2:
                session[f'resp_{passo}'] = "sim" in pergunta
                proximo = passo + 1
                if proximo in PERGUNTAS_AKINATOR:
                    session['passo'] = proximo
                    return jsonify({"resposta": PERGUNTAS_AKINATOR[proximo]})
                else:
                    r1, r2 = session.get('resp_2'), session.get('resp_3')
                    session.clear()
                    if r1 and not r2: return jsonify({"resposta": "Aposto que você pensou no Neymar Jr!"})
                    if not r1 and r2: return jsonify({"resposta": "Você pensou no Homem de Ferro!"})
                    return jsonify({"resposta": "Dedução final: Você pensou em alguém incrível! Digite 'Akinator' para jogar de novo."})

        # --- DATA E HORA ---
        agora = datetime.now(timezone)
        if "que horas são" in pergunta: return jsonify({"resposta": f"Agora são {agora.strftime('%H:%M')}."})
        if "que dia é hoje" in pergunta: return jsonify({"resposta": f"Hoje é {agora.strftime('%d/%m/%Y')}."})
        if "quem é você" in pergunta: return jsonify({"resposta": "Eu sou a Geometry AI, sua assistente virtual focada em educação e programação."})

        # --- DICIONÁRIO DE COMANDOS ---
        comandos = {
            "bom dia": "Bom dia! Pronto para os desafios de hoje?",
            "boa tarde": "Boa tarde! Como está seu progresso hoje?",
            "boa noite": "Boa noite! Não esqueça de descansar os olhos.",
            "quem te criou": "Fui criada pelo desenvolvedor Guester_DEV.",
            "o que é python": "Uma linguagem de programação poderosa e fácil de aprender.",
            "o que é java": "Uma linguagem robusta usada em grandes sistemas e Android.",
            "o que é git": "Um sistema de controle de versão para programadores.",
            "o que é docker": "Uma plataforma que empacota software em containers.",
            "o que é algoritmo": "Uma sequência de passos para resolver um problema.",
            "o que é bug": "Um erro inesperado em um software.",
            "capital da frança": "Paris.", "capital da alemanha": "Berlim.",
            "capital do japão": "Tóquio.", "capital da itália": "Roma.",
            "maior país": "Rússia.", "maior rio": "Rio Amazonas.",
            "o que é átomo": "A menor unidade da matéria comum.",
            "quem foi einstein": "Físico que criou a teoria da relatividade.",
            "o que é dna": "Molécula que contém nossas instruções genéticas.",
            "quem é harry potter": "O bruxo protagonista da obra de J.K. Rowling.",
            "quem é darth vader": "O icônico vilão da saga Star Wars.",
            "quem é o homem-aranha": "Peter Parker, o herói da Marvel que escala paredes.",
            "maior animal do mundo": "Baleia-azul.",
            "me conte uma piada": "Por que o computador foi ao médico? Porque estava com vírus!",
            "tchau": "Até logo! Estarei aqui quando precisar.",
            "obrigado": "Por nada! Fico feliz em ajudar."
        }

        # --- NOVO COMANDO: LISTA DE COMANDOS (DINÂMICO) ---
        if "lista de comandos" in pergunta or "o que você faz" in pergunta:
            # Pega todas as chaves do dicionário e organiza em texto
            lista_formatada = ", ".join(sorted(comandos.keys()))
            return jsonify({"resposta": f"📋 **Aqui estão os comandos que eu entendo instantaneamente:**\n\n{lista_formatada}\n\nAlém disso, posso pesquisar qualquer outra coisa na web e jogar **Akinator**!"})

        # Verificação de comandos fixos
        for chave, valor in comandos.items():
            if chave in pergunta:
                return jsonify({"resposta": valor})

        # --- CLIMA ---
        if "clima em" in pergunta:
            with DDGS() as ddgs:
                res = list(ddgs.text(f"previsão do tempo hoje em {pergunta}", region='br-pt', max_results=1))
                return jsonify({"resposta": res[0]['body'] if res else "Erro ao consultar clima."})

        # --- PESQUISA WEB ---
        with DDGS() as ddgs:
            res = list(ddgs.text(pergunta, region='br-pt', max_results=1))
            if res:
                return jsonify({"resposta": f"{res[0]['body']}\n\nFonte: DuckDuckGo"})

        return jsonify({"resposta": "Não entendi sua pergunta. Tente 'Lista de comandos'!"})

    except Exception as e:
        return jsonify({"resposta": f"Erro: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
            "boa tarde": "Boa tarde! Preparado para programar algo novo?",
            "boa noite": "Boa noite! Não esqueça de descansar os olhos da tela.",
            "abrir google": "Você pode acessar em google.com",
            "valor do dólar": "O câmbio muda toda hora. Recomendo pesquisar 'Dólar hoje'.",
            "raiz quadrada de 144": "A raiz quadrada de 144 é 12.",
            "o que é html": "HTML é a linguagem de marcação que estrutura as páginas da web.",
            "o que é css": "CSS é o que dá estilo, cores e layout para o HTML.",
            "como aprender a programar": "Comece com lógica de programação e depois escolha uma linguagem como Python.",
            "dica de estudo": "Pratique 30 minutos todos os dias em vez de 5 horas uma vez por semana.",
            "frase do dia": "A persistência é o caminho do êxito!",
            "está acordada": "Sempre! Estou rodando nos servidores do Render agora mesmo.",
            "me ajude": "Claro! Digite sua dúvida sobre matemática, história ou programação.",
            "limpar chat": "Basta recarregar a página para limpar nossa conversa.",
            "quem descobriu o brasil": "Pedro Álvares Cabral, em 1500.",
            "maior país do mundo": "A Rússia é o maior país em extensão territorial.",
            "capital da frança": "A capital da França é Paris.",
            "quantos planetas existem": "No nosso sistema solar, temos 8 planetas.",
            "o que é javascript": "É a linguagem que traz interatividade para os sites.",
            "o que é o render": "Render é a plataforma onde eu estou hospedada agora!",
            "gosta de música": "Eu gosto de sons binários e Lo-fi para programar.",
            "tchau": "Até logo! Estarei aqui se precisar.",
            "obrigado": "Por nada! Fico feliz em ajudar."
        }

        for cmd, resposta in comandos_diretos.items():
            if cmd in pergunta:
                return jsonify({"resposta": resposta})

        # BUSCA PADRÃO (DUCKDUCKGO)
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pergunta, region='br-pt', max_results=1))
            if resultados:
                return jsonify({"resposta": resultados[0]['body']})

        return jsonify({"resposta": "Ainda estou aprendendo sobre isso. Pode perguntar de outra forma?"})

    except Exception as e:
        return jsonify({"resposta": f"Erro técnico: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
        
