# Curl to Robot Framework Converter

Conversor de comandos cURL para código Robot Framework. Esta ferramenta automatiza a criação de keywords para testes de API no Robot Framework a partir de comandos cURL.

## 🚀 Funcionalidades
- Extrai URLs e headers de arquivos cURL
- Detecta automaticamente o tipo de corpo da requisição (JSON, form-data, urlencoded)
- Gera código Robot Framework pronto para uso
- Suporte a requisições com arquivos (multipart/form-data)
- Interface interativa via terminal

## 📋 Pré-requisitos
- Python 3.8+

## ⚙️ Instalação
- Clone o repositório ou salve o arquivo Python localmente

## 🛠 Uso
Execute o script e siga as instruções interativas:

```bash
python curl_to_robot.py
```

## Fluxo de trabalho:

- Forneça o caminho para o arquivo contendo o comando cURL

- Informe o caminho de saída para o arquivo Robot Framework (.robot)

- O script detectará automaticamente o tipo de requisição

- Para requisições form-data, informe se há arquivos envolvidos

## Exemplo de entrada (cURL):
```bash
curl 'https://api.example.com/data' \
  --header 'Authorization: Bearer token' \
  --header 'Content-Type: application/json' \
  --data-raw '{"key":"value"}'
```

## Saída gerada (Robot Framework):
```bash
Keyword Name Here
    Create Session    session    https://api.example.com/data
    
    ${headers}=    Create Dictionary
    ...    Authorization=Bearer token
    ...    Content-Type=application/json
    
    ${body}=    Set Variable    {"key":"value"}
    
    ${response}=    REQUEST On Session    session    /
    ...    headers=${headers}
    ...    data=${body}
```

## 📄 Licença
#### Distribuído sob a licença MIT. Veja LICENSE para mais informações.