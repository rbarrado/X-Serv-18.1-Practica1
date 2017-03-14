#!/usr/bin/python3

"""
webApp class
 Root for hierarchy of classes implementing web applications
 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2017
"""

import socket
import webapp
import csv
import os


class AcortaUrlsApp (webapp.webApp):
	"""Simple web application for managing content.
	Content is stored in a dictionary, which is intialized
	with the web content."""
	contador = -1
	urls = {}
	urls_acortadas = {}
    
	def writeURL(self,urlLarga,urlCorta):
		with open("fich.csv", "a") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([int(urlCorta)] + [urlLarga])
		return None

	def readDicc(self,file):
		with open('fich.csv', 'r') as csvfile:
			if os.stat('fich.csv').st_size == 0:
				print("Empty file")
			else:
				reader = csv.reader(csvfile)
				for row in reader: #siguiendo lo que hemos hecho, row[0] = urlshort y row[1] = urlLong
					self.urls_acortadas[row[1]] = int(row[0])
					self.urls[int(row[0])] = row[1]
					self.contador = self.contador + 1
				return None 

	def parse(self, request):
		"""Parse the received request, extracting the relevant information."""

		metodo = request.split(" ")[0]
		resource = request.split(" ")[1]
        
		if metodo == "POST":
			body = request.split('\r\n\r\n', 1)[1]
			body = body.split("=")[1].replace("+", " ")
		elif metodo == "GET":
			body = ""

		return (metodo, resource, body)

	def process(self, resourceName):
		
		global httpCode, htmlBody

		(metodo, resource, body) = resourceName
		formulario = '<form action="" method="POST">'
		formulario += 'Url acortada: <input type="text" name="valor">'
		formulario += '<input type="submit" value="Enviar">'
		formulario += '</form>'

		if len(self.urls_acortadas) == 0:
			self.readDicc('fich.csv')
		if metodo == "GET":
			if resource == "/":
				httpCode = "200 OK"
				htmlBody = "<html><body>" + formulario\
								+ "<p>" + str(self.urls_acortadas)\
								+ "</p></body></html>"
			else:
				try:
					resource = int(resource[1:])
					if resource in self.urls:
						httpCode = "300 Redirect"
						htmlBody = "<html><body><meta http-equiv='refresh'"\
										+ "content='1 url="\
										+ self.urls[resource] + "'>"\
										+ "</p>" + "</body></html>"
					else:
						httpCode = "404 Not Found"
						htmlBody = "<html><body>"\
										+ "Error: Resource not available"\
										+ "</body></html>"
				except ValueError:
					httpCode = "404 Not Found"
					htmlBody = "<html><body>"\
									+ "Error: Resource not available"\
									+ "</body></html>"

			return (httpCode, htmlBody)

		elif metodo == "POST":
			print(body)

			if body == "":
				httpCode = "404 Not Found"
				htmlBody = "<html><body>"\
								+ "Error: NO hay URLS"\
		                  + "</body></html>"
				return(httpCode, htmlBody)
			elif body.find("http") == -1:
				body = "http://" + body
				while body.find("%2F") != -1:
					body = body.replace("%2F", "/")
				self.contador = self.contador + 1
				contador = self.contador
				self.urls_acortadas[body] = contador
				self.urls[contador] = body
				self.writeURL(body,contador)
				httpCode = "200 OK"
				htmlBody = "<html><body>"\
							+ "<a href=" + body + ">" + body + "</href>"\
							+ "<p><a href=" + str(contador) + ">" + str(contador)\
							+ "</href></body></html>"
			else:
				while body.find("%2F") != -1:
					body = body.replace("%2F", "/")
					if body in self.urls_acortadas:
						contador = self.urls_acortadas[body]
						self.contador = self.contador + 1
						contador = self.contador
						self.urls_acortadas[body] = contador
						self.urls[contador] = body
						self.writeURL(body,contador)
						httpCode = "200 OK"
						htmlBody = "<html><body>"\
									+ "<a href=" + body + ">" + body + "</href>"\
									+ "<p><a href=" + str(contador) + ">" + str(contador)\
									+ "</href></body></html>"
					else:
						body = "http://" + body[9:]
						self.contador = self.contador + 1
						contador = self.contador
						self.urls_acortadas[body] = contador
						self.urls[contador] = body
						self.writeURL(body,contador)
						httpCode = "200 OK"
						htmlBody = "<html><body>"\
									+ "<a href=" + body + ">" + body + "</href>"\
									+ "<p><a href=" + str(contador) + ">" + str(contador)\
									+ "</href></body></html>"
			print(self.urls_acortadas)
			return (httpCode, htmlBody)
		else:
			httpCode = "404 Not Found"
			htmlBody = "<html><body>Metodo no soportado</body></html>"
			return (httpCode, htmlBody)

if __name__ == "__main__":
    try:
        testWebApp = AcortaUrlsApp("localhost", 1234)
    except KeyboardInterrupt:
        print ("")
        print ("Finish")
