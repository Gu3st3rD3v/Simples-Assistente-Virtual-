# Simples-Assistente-Virtual-
Simples Assistente virtual, uso livre.

Este é um projeto de uma Assistente Virtual básica desenvolvida para rodar na web. A aplicação utiliza Python (Flask) no backend e uma interface moderna construída com HTML5, CSS3 e JavaScript (ES6).

Como a Assistente Funciona?

O funcionamento segue o fluxo "Client-Server" (Cliente-Servidor):

1. Interface (Frontend): O usuário digita uma mensagem no campo de texto do index.html.

2. Envio (JavaScript): O arquivo script. js captura esse texto e envia uma requisição assíncrona (usando fetch) para o servidor Python.

3. Processamento (Backend): O servidor Flask (app. py) recebe a pergunta, processa a lógica de resposta (que pode ser uma lógica simples de "se/então" ou uma chamada de API como o Gemini) e devolve um objeto JSON. O JavaScript recebe esse JSON e cria dinamicamente um novo "balão de fala" no chat para exibir a resposta da assistente.
