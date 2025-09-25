# !pip install requests beautifulsoup4 openai langchain-openai

import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    for script_or_style in soup(['script', 'style']):
      script_or_style.decompose()
    texto = soup.get_text(separator= ' ')
    #Limpar texto
    linhas = (linha.strip() for linha in texto.splitlines())
    parts = (parte.strip() for linha in linhas for parte in linha.split(' '))
    texto_limpo = '\n'.join(parte for parte in parts if parte)
    return texto_limpo
  else:
    print(f"failed to fetch the URL. Status code: {response.status_code}")
    return None

extract_text_from_url('https://dev.to/miguelparacuellos/openai-just-went-open-source-for-real-this-time-2dao')

from langchain_openai.chat_models.azure import AzureChatOpenAI

client = AzureChatOpenAI (
    azure_endpoint = "ENDPOINT HERE",
    api_key = "API KEY HERE",
    api_version = "2024-02-15-preview",
    deployment_name = "gpt-4o-mini",
    max_retries = 0
)

def translate_article(text, lang):
  messages = [
      ("system", "Você atua como tradutor de textos"),
      ("user", f"Traduza o {text} para o idioma {lang} e responda em markdown")
  ]

  response = client.invoke(messages)
  print(response.content)
  return response.content
translate_article("Let's see if he deployment was succeed", "portugues")

url = 'https://dev.to/miguelparacuellos/openai-just-went-open-source-for-real-this-time-2dao'
text = extract_text_from_url(url)
article = translate_article(text, "portugues")
print(article)

