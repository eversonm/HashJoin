import re
import os
import time

def funcaoHash(elem = 1):
	#m = 2047
	m = 16383
	chave = elem % m
	return chave
#Essa funcaoHash foi utilizada para diminuir o custo com processamento

def funcaoHashUniversal(x = 0):
	a = 30
	b = 45
	p = 4091
	m = 1023
	chave_hash = ((a*x + b)% p) % m
	return chave_hash

"""
varrerTAB eh uma funcao utilizada para gerar a tabela hash e os buckets para juncao hash posterior.

"""
def varrerTab(tabela = "arq.txt", indice=0,diretorio = "TabelaA/"):
	inicio = time.time()
	arquivo = open(tabela, "r")
	arq_tab_hash = open("TabelaHash.txt", "w+")
	arq_tab_hash.close()
	for linha_arquivo in arquivo:
		capt_chave = capChave(linha_arquivo,indice)
		chave = funcaoHash(capt_chave)
		tab_hash(chave)
		arq_bucket_criacao = criarBucket(chave,diretorio)
		preencher_bucket = preencherBucket(linha_arquivo, arq_bucket_criacao, diretorio)
	arquivo.close()

	fim = time.time()
	print("Tempo total para fazer hash da tabela: ",fim-inicio)

"""
varrerTab2 eh utilizada para gerar a tabela hash de uma juncao ja efetuada anteriormente
removendo caracteres especiais delimitadores [tuplaTAB1][tuplaTAB2] e gerando os buckets
da primeira juncao efetuada.

"""
def varrerTab2(tabela = "arq.txt", indice=0,diretorio = "TabelaAB/"):
	inicio = time.time()
	arquivo = open(tabela, "r")
	arq_tab_hash = open("TabelaHash.txt", "w+")
	arq_tab_hash.close()
	for linha_arquivo in arquivo:
		linha_arquivo = re.sub("['(),.]","",linha_arquivo)
		linha_arquivo = linha_arquivo.replace("[","")
		linha_arquivo = linha_arquivo.replace("]","")
		capt_chave = capChave(linha_arquivo,indice)
		chave = funcaoHash(capt_chave)
		tab_hash(chave)
		arq_bucket_criacao = criarBucket(chave,diretorio)
		preencher_bucket = preencherBucket(linha_arquivo, arq_bucket_criacao, diretorio)
	arquivo.close()

	fim = time.time()
	print("Tempo total para fazer hash da tabela: ",fim-inicio)



def capChave(tupla = "0, cidade, UF", indicevetor = 0):
	tuplaF = tupla.split()
	vetor = tuplaF[indicevetor]

	return int(vetor) #ou a posicao desejada do vetor


def tab_hash(chave):
	tabela_hash = open("TabelaHash.txt", "a+")
	chave = str(chave)+'\n'

	if chave not in tabela_hash:
		tabela_hash.write(chave)
	tabela_hash.close()


def criarBucket(valor, diretorio="TabelaA/"):
	nomearq = "Bucket" + str(valor) + ".txt"
	if os.path.exists(nomearq):
		return nomearq
	arq_bucket = open(diretorio+nomearq, "a+")
	arq_bucket.close()
	return nomearq


def preencherBucket(tuplaInteira, nomearq, diretorio="TabelaA/"):
	bucket = open(diretorio+nomearq, "a+")
	bucket.write(tuplaInteira)
	bucket.close()

"""
funcaoJuncaoAB efetua a juncao dos buckets referentes a tabA e a tabB.
Esses buckets sao criados nas pastas respectivas ao seu nome e a juncao
eh salva na pasta TabelaAB
"""
def funcaoJuncaoAB(atriJuncaoA, atriJuncaoB, indice):
	try:
		bucketA = open("TabelaA/Bucket"+str(indice)+".txt","r")
		tabAB = open("TabelaAB/TabelaAB.txt","a+")
		for A in bucketA:
			linhaA = A.split()
			try:
				bucketB = open("TabelaB/Bucket"+str(indice)+".txt","r")
				for B in bucketB:
					linhaB = B.split()
					if (linhaA[atriJuncaoA]==linhaB[atriJuncaoB]):
						tabAB.write(str(linhaA)+str(linhaB)+"\n")
			except:
				bucketA.close()
				tabAB.close()

			bucketB.close()
		bucketA.close()
		tabAB.close()
	except:
		indice=indice 
		#Nao faca nada e saia da funcao


"""
funcaoJuncaoABC efetua a juncao dos buckets referentes a tabAB e a tabC.
A tabAB eh o resultado da primeira juncao e ela deve ser utilizada para 
gerar os buckets para a juncaoABC

Esses buckets sao criados nas pastas respectivas ao seu nome e a juncao
eh salva na pasta TabelaABC
"""
def funcaoJuncaoABC(atriJuncaoAB, atriJuncaoC, indice):
	try:
		bucketAB = open("TabelaAB/Bucket"+str(indice)+".txt","r")
		tabABC = open("TabelaABC/TabelaABC.txt","a+")

		for linha in bucketAB:
			
			linha = re.sub("['(),.]","",linha)
			linha = linha.replace('[',' ')
			linha = linha.replace(']','')
			linhaAB = linha.split()
		
			try:
				bucketC = open("TabelaC/Bucket"+str(indice)+".txt","r")
				for C in bucketC:
					linhaC = C.split()
					if (linhaAB[atriJuncaoAB]==linhaC[atriJuncaoC]):
						tabABC.write(str(linhaAB)+str(linhaC)+"\n")
		
				bucketC.close()
			
			except:
				bucketAB.close()
				tabABC.close()

		bucketAB.close()
		tabABC.close()
	
	except:
		indice = indice
		#Nao faca nada e saia da funcao


#formato do diretório: TabelaAB/
def qtdeArquivosPasta(diretorio="TabelaA/"):
	vetor=""
	for _, _, arquivo in os.walk(''+diretorio+''):
		vetor = vetor + str(arquivo) +" "
	
	v = len(vetor.split())
	return v

#jun = qtdeArquivosPasta()
def lerHashJuncao(atrA,atrB,v):
	inicio = time.time()
	abrir = open("TabelaHash.txt", "r")
	v = 0
	for line in abrir:
		v = int(line.replace("\n","")) #v recebe o valor da chave da tabela hash
		funcaoJuncaoABC(atrA,atrB, v) #juncao eh feita sobre esse valor da hash
	fim = time.time()
	print("Tempo total para juncao: ",fim-inicio)


#cria os diretorios para o usuario
def criarDiretorios():
	try:	
		os.mkdir('TabelaA')
		os.mkdir('TabelaB')
		os.mkdir('TabelaC')
		os.mkdir('TabelaAB')
		os.mkdir('TabelaABC')
	except:
		print("Erro ao criar os diretorios!!!")

"""
varrerTabMem eh um prototipo de funcao que pode fazer uma varredura em busca de
criar os buckets num espaco de tempo menor. O atributo "passo" eh a quantidade de
atributos que uma tabela possui. Ex: nation possui 4 atributos.
"""

def varrerTabMem(tabela = "arq.txt", indice=0,diretorio = "TabelaA/",passo = 10):
	inicio = time.time()
	a = open(tabela, "r")
	carregaArqMEM = a.read()
	v = []
	v =carregaArqMEM.split()
	tamanho = len(v)

	matrizShow = [""]*16383
	#matrizshow eh a matriz que vai comportar toda a tabela em memoria.
	tabhash = []
	#tabhash eh o vetor que vai receber a chave hash de cada iteracao.
	
	arq_tab_hash = open("TabelaHash.txt", "w+")
	arq_tab_hash.close()
	#Abrir a TabelaHash e fecha-la serve apenas para apagar o conteudo do arquivo.

	for i in range(0,tamanho,passo):
		linha = []
		#string = v[i]+" "+v[i+1]+" "+v[i+2]+" "+v[i+3]+" "+v[i+4]#+" "+v[i+5]+" "+v[i+6]+" "+v[i+7]#+" "+v[i+8]#+" "+v[i+9]
		for l in range(0,passo):
			if l+1 == passo:
				#string = v[i]+" "+...+" "+v[n] onde 0<=i<=n
				string = v[i]
			string = v[i]+" "

		capt_chave = capChave(string,indice)
		chave = funcaoHash(capt_chave)
		tabhash.append(chave)
		matrizShow[chave] = matrizShow[chave] + str(string+"\n")

	fim = time.time()
	print("Carregar a tabela em memoria e fazer hash em memoria: ", fim-inicio)
	
	inicio = time.time()
	
	#Vetor hashe recebe a tabela hash em memoria
	hashe = []
	
	hashe = set(tabhash)
	#eliminar elementos duplicados de tabhash
	hashe = list(hashe)
	#tornar hashe uma lista
	
	t = len(hashe)
	for index in range(0,t):
		tab_hash(hashe[index])
	
	aux = (len(matrizShow))
	
	arquivo = open("TabelaHash.txt", "r")
	v = 0
	#para cada posicao da tabela hash (hashe)
	for v in hashe:
		#v = int(linha.replace("\n",""))
		if (matrizShow[v] == ""):
			v = v #Dado que a posicao(v) da matriz eh vazia, nao faca nada
		else:
			#abra o bucket e o preencha com o conteudo da matriz na posicao v
			nomearq = "Bucket" + str(v) + ".txt"
			preencherBucket(matrizShow[v],nomearq,diretorio)

	fim = time.time()
	print("Tempo total para varrer tabela usando memoria: ",fim-inicio)


"""
joinMAX eh uma funcao que executa todos os procedimentos de uma juncao especifica

select * 
from nation inner join region inner join customer
on n_regionkey=r_regionkey 
on n_nationkey=c_nationkey

"""
def joinMAX():
	varrerTab("nation.txt",d["n_regionkey"],"TabelaA/")
	varrerTab("region.txt",d["r_regionkey"],"TabelaB/")
	v = qtdeArquivosPasta("TabelaA")
	
	inicio = time.time()
	abrir = open("TabelaHash.txt", "r")
	v = 0
	for line in abrir:
		v = int(line.replace("\n",""))
		funcaoJuncaoAB(d["n_regionkey"],d["r_regionkey"], v)
	fim = time.time()
	print("Tempo total para juncao 1: ",fim-inicio)	


	varrerTab2("TabelaAB/TabelaAB.txt",d["n_nationkey"],"TabelaAB/")
	varrerTab("customer.txt",d["c_nationkey"],"TabelaC/")
	v = qtdeArquivosPasta("TabelaC")
	
	inicio = time.time()
	abrir = open("TabelaHash.txt", "r")
	v = 0
	for line in abrir:
		v = int(line.replace("\n",""))
		funcaoJuncaoABC(d["n_nationkey"],d["c_nationkey"], v)
	fim = time.time()
	print("Tempo total para juncao 2 (final): ",fim-inicio)	
