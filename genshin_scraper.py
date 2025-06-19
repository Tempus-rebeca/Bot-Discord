import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extrair_data_publicacao(data_str):
    for fmt in ("%Y/%m/%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(data_str, fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return datetime.now().strftime("%d/%m/%Y")

def extrair_duracao_evento(url_evento):
    try:
        resp = requests.get(url_evento, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')

        duracao_h4 = soup.find('h4', string=lambda s: s and "Duração do Evento" in s)
        if duracao_h4:
            duracao_p = duracao_h4.find_next_sibling('p')
            if duracao_p:
                return duracao_p.text.strip()
    except Exception as e:
        print(f"[Erro] Ao buscar duração do evento: {e}")
    return None

def buscar_eventos_genshin():
    url = "https://www.hoyolab.com/circles/2/27/official?page_type=27&page_sort=news"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[Erro] Falha ao buscar eventos: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    eventos = []

    for post in soup.select('.list-item'):
        titulo_el = post.select_one('.title')
        data_el = post.select_one('.time')
        link_el = post.select_one('a')

        if not titulo_el or not data_el or not link_el:
            continue

        titulo = titulo_el.text.strip()
        data_texto = data_el.text.strip()
        data_pub = extrair_data_publicacao(data_texto)
        link = "https://www.hoyolab.com" + link_el['href']

        if 'event' in titulo.lower():
            duracao = extrair_duracao_evento(link)
            eventos.append({
                "titulo": titulo,
                "link": link,
                "data_publicacao": data_pub,
                "duracao_evento": duracao or "Não encontrada"
            })

            time.sleep(1)

    return eventos
