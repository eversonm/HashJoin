import re
import os
import pyodbc
import getpass
from funcoes import *
from conexaosql import *

os.system('cls')

#Dicionario para facilitar escolha dos atributos de juncao
d = {
"n_nationkey" : 0, "n_name" : 1, "n_regionkey" : 2, "n_comment" : 3, 
"o_orderkey" : 0, "o_custkey" : 1, "o_orderstatus" : 2, "o_totalprice" : 3, "o_orderDATE" : 4, "o_orderpriority" : 5, "o_clerk" : 6, "o_shippriority" : 7, "o_comment" : 8, 
"c_custkey" : 0, "c_name" : 1, "c_address" : 2, "c_nationkey" : 3, "c_phone" : 4, "c_acctbal" : 5, "c_mktsegment" : 6, "c_comment" : 7, 
"r_regionkey" : 0, "r_name" : 1, "r_comment" : 2, 
"l_orderkey" : 0, "l_partkey" : 1, "l_suppkey" : 2, "l_linenumber" : 3, "l_quantity" : 4, "l_extendedprice" : 5, "l_discount" : 6, "l_tax" : 7, "l_returnflag" : 8, "l_linestatus" : 9, "l_shipDATE" : 10, "l_commitDATE" : 11, "l_receiptDATE" : 12, "l_shipinstruct" : 13, "l_shipmode" : 14, "l_comment" : 15, 
"p_partkey" : 0, "p_name" : 1, "p_mfgr" : 2, "p_brand" : 3, "p_type" : 4, "p_size" : 5, "p_container" : 6, "p_retailprice" : 7, "p_comment" : 8, 
"ps_partkey" : 0, "ps_suppkey" : 1, "ps_availqty" : 2, "ps_supplycost" : 3, "ps_comment" : 4, 
"s_suppkey" : 0, "s_name" : 1, "s_address" : 2, "s_nationkey" : 3, "s_phone" : 4, "s_acctbal" : 5, "s_comment" : 6
}


##################CRIAR DIRETORIOS###################
criarDiretorios()
#####################################################

#################CONEXAO COM O BANCO#################
c = conexaoBanco()
selecionarTABELA(c,"nation")
selecionarTABELA(c,"region")
selecionarTABELA(c,"customer")

#####################################################


#################VARRENDO tabA e tabB################
varrerTab("nation.txt",d["n_regionkey"],"TabelaA/")
varrerTab("region.txt",d["r_regionkey"],"TabelaB/")
v = qtdeArquivosPasta("TabelaA")

inicio = time.time()
abrir = open("TabelaHash.txt", "r")
v = 0

#################JOIN DAS AS TABELAS#################
for line in abrir:
	v = int(line.replace("\n",""))
	funcaoJuncaoAB(d["n_regionkey"],d["r_regionkey"], v)
fim = time.time()
#JUNCAO 1
print("Tempo total para juncao 1: ",fim-inicio)	


################VARRENDO tabAB e tabC################
varrerTab2("TabelaAB/TabelaAB.txt",d["n_nationkey"],"TabelaAB/")
varrerTab("customer.txt",d["c_nationkey"],"TabelaC/")
v = qtdeArquivosPasta("TabelaC")

inicio = time.time()
abrir = open("TabelaHash.txt", "r")
v = 0

#################JOIN DAS AS TABELAS#################
for line in abrir:
	v = int(line.replace("\n",""))
	funcaoJuncaoABC(d["n_nationkey"],d["c_nationkey"], v)
fim = time.time()
#JUNCAO 2
print("Tempo total para juncao 2 (final): ",fim-inicio)	

#####################################################



#####################################################

#varrerTabMem("customer.txt",d["c_nationkey"],"TabelaB/", 5)
#joinMAX()
#varrerTabMem("lineitem2.txt",d["l_orderkey"],"TabelaA/", 5)
#varrerTabMem("lineitem2.txt",d["l_orderkey"],"TabelaA/", 5)