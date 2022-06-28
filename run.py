import requests
import bs4
import re
import json
from pathlib import Path
from datetime import date  
from flask import Flask,jsonify
import time
# import requests
# import bs4
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
# link = "https://www.promiedos.com.ar/"
# res = requests.get(link,headers=headers)
# soup = bs4.BeautifulSoup(res.text, 'html.parser')

# soup.select('#principal #partidos div #fixturein table tr')[1]

app = Flask(__name__) 

@app.route('/',methods=['GET'])
def home_page():
	time.sleep(1)
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
	link = "https://www.promiedos.com.ar/"

	res = requests.get(link,headers=headers)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')

	ligas_jugando = soup.select('#principal #partidos div #fixturein table')
	datos = []


	for liga in ligas_jugando:
		nombre_liga = liga.select('tr')[1].text.strip()
		bandera_liga = liga.select('td a')[0].select('img')[0]['src']
		partidos = liga.select('tr')
		cantidad_partidos = (len(partidos)-2)/2
		# print(nombre_liga,cantidad_partidos)
		liga_obj = {
			"nombre_liga":nombre_liga,
			"bandera_liga":bandera_liga,
			"partidos":[]
		}

		for i in range(2,len(partidos),2):
			hora = partidos[i].select('td')[0].text.strip()
			estado_partido = ''
			ficha = ''

			clase = partidos[i].select('td')[0]['class'][0]
			if clase == 'game-fin':
				estado_partido = 'terminado'
			elif clase == 'game-play':
				estado_partido = 'jugando'
			elif estado_partido == 'game-time':
				estado_partido = 'no empezado'

			if partidos[i].select('td')[5].text != '':
				ficha = partidos[i].select('td')[5].select('a')[0]['href']

			equipo1 = partidos[i].select('td')[1].select('span')[0].text
			escudo1 = partidos[i].select('td')[1].select('img')[0]['src']
			rojas1 = len(partidos[i].select('td')[2].select('.rojas1')[0].select('.roja'))

			cantidad_goles1 = partidos[i].select('td')[2].select('span')[0].text
			autores1 = []
			if partidos[i+1].select('td')[0] != '':
				i_tag = partidos[i+1].select('td')[0].select('i')
				array_minutos = []
				for j in i_tag:
					array_minutos.append(j.text)
				for j in i_tag: #sacar?
					partidos[i+1].select('td')[0].i.decompose()
				nombres_autores = re.split(";",partidos[i+1].select('td')[0].text.strip()[:-1])
				for h in range(len(nombres_autores)):
					nombres_autores[h] = nombres_autores[h].strip()

				for g in range(len(array_minutos)):
					autores1.append({
						"minuto":array_minutos[g],
						"autor":nombres_autores[g]
					})
			else:
				array_minutos = 0
				nombres_autores = ''

			equipo2 = partidos[i].select('td')[4].select('span')[0].text
			escudo2 = partidos[i].select('td')[4].select('img')[0]['src']
			rojas2 = len(partidos[i].select('td')[3].select('.rojas2')[0].select('.roja'))

			cantidad_goles2 = partidos[i].select('td')[3].select('span')[0].text
			autores2 = []
			if partidos[i+1].select('td')[1] != '':
				i_tag = partidos[i+1].select('td')[1].select('i')
				array_minutos = []
				for j in i_tag:
					array_minutos.append(j.text)
				for j in i_tag: #sacar?
					partidos[i+1].select('td')[1].i.decompose()
				nombres_autores = re.split(";",partidos[i+1].select('td')[1].text.strip()[:-1])
				for h in range(len(nombres_autores)):
					nombres_autores[h] = nombres_autores[h].strip()

				for g in range(len(array_minutos)):
					autores2.append({
						"minuto":array_minutos[g],
						"autor":nombres_autores[g]
					})
			else:
				array_minutos = 0
				nombres_autores = ''

			partido_obj = {
				"hora":hora,
				"estado_partido":estado_partido,
				"ficha":ficha,
				"equipo_local":{
					"nombre_equipo":equipo1,
					"escudo":escudo1,
					"cantidad_goles":cantidad_goles1,
					"autores":autores1,
					"rojas":rojas1
				},
				"equipo_visitante":{
					"nombre_equipo":equipo2,
					"escudo":escudo2,
					"cantidad_goles":cantidad_goles2,
					"autores":autores2,
					"rojas":rojas2
				}
			}

			liga_obj["partidos"].append(partido_obj)

		datos.append(liga_obj)

	return jsonify(datos)

# if __name__ == '__main__':
# 	app.run(port=7777)

#fecha = date.today().isoformat()
# ruta = Path(__file__).parent.resolve().joinpath('partidos_'+fecha+'.json')
# archivo = open(ruta,'w',encoding='utf-8')
# archivo.write(datos)
# archivo.close()
# print('Ok')


    


