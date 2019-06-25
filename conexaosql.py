#!"/Users/M0US3/AppData/Local/Programs/Python/Python37-32/python.exe"   

import pyodbc
import getpass
import re
import time
import os
import _thread

os.system('cls')

def conexaoBanco():
	senha = getpass.getpass('Entre com a senha do SQL Server: ')
	
	conexaoBanco = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};'
	                      'SERVER=ULTRAPC\SQLEXPRESS;'
	                      'DATABASE=tpc_h;'
	                      'UID=sa;'
	                      'PWD='+senha+';'
	                      'Trusted_Connection=yes;')

	cursor = conexaoBanco.cursor()
	return cursor


###############Carregando tabela em arquivo.txt########

def selecionarTABLE(cursor):
	tab = input("Entre com o nome da tabela do banco de dados tpc_h: ")
	arqtab = tab + ".txt"
	arquivo = open(arqtab, "a+")
	inicio = time.time()
	cursor.execute("SELECT * from "+tab+"")

	for row in cursor:
		auxiliar = str(row) + ' ' + "\n"
		#print(auxiliar)
		auxiliar = re.sub("[ .()]", "", auxiliar)
		auxiliar = re.sub(",", " ",auxiliar)
		auxiliar = re.sub(",", "",auxiliar)
		auxiliar = re.sub("'", "", auxiliar)
		arquivo.write(str(auxiliar))

	fim = time.time()
	print("Tempo total para selecionar tabela "+tab+": ",fim-inicio)
	return tab


def selecionarTABELA(cursor, tab):
	arqtab = tab + ".txt"
	arquivo = open(arqtab, "a+")
	inicio = time.time()
	cursor.execute("SELECT ps_partkey,ps_suppkey,ps_availqty,ps_supplycost from "+tab+"")

	for row in cursor:
		auxiliar = str(row) + ' ' + "\n"
		#print(auxiliar)
		auxiliar = re.sub("[(.)]", "", auxiliar)
		auxiliar = re.sub(" ", "",auxiliar)
		auxiliar = re.sub(",", " ",auxiliar)
		auxiliar = re.sub(",", "",auxiliar)
		auxiliar = re.sub("'", "", auxiliar)
		arquivo.write(str(auxiliar))

	fim = time.time()

	print("Tempo total para selecionar tabela "+tab+": ",fim-inicio)
	return tab


def mostrarAtribTabela(cursor, tabela = 'name'):
	cursor.execute("SELECT column_name from information_schema.columns where table_name = '"+tabela+"'")
	auxiliar = ''
	i = 0
	for row in cursor:
		tupla = '['+str(i)+']'+str(row) + ' '
		auxiliar = auxiliar + tupla
		#aux = re.sub("[],[',()]", "", aux)
		auxiliar = re.sub("[,(')]", '', auxiliar)
		i=i+1
	print(auxiliar, end = "")
	print("\n")
	#return auxiliar


##################SQL SERVER###############

"""
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:myserver.database.windows.net' 
database = 'mydb' 
username = 'myusername' 
password = 'mypassword' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()    

SELECT * FROM sys.columns WHERE object_id = object_id('nation')
"""