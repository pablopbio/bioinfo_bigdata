#!/usr/bin/python
#Ejercico_BIGDATA
#B''H

#Campos a extraer:
#1.- Identificador principal: DBSOURCE REFSEQ: The Reference Sequence (RefSeq) collection provides a
# comprehensive, integrated, non-redundant, well-annotated set of sequences, including genomic DNA, 
# transcripts, and proteins.
#2.- Nombre del gen -> gene_name.
#3.- Identificador taxonomico -> taxa.
#4.- Fuente de la anotacion -> data_basexref-grupo1
#5.- Anotacion como tal -> data_basexref-grupo1

#Importamos modulos necesarios (sys, re).
import sys
import re

#Generamos ficheros necesarios(tabular_* para datos y seq_* para secuencias fasta.
filehandle = open('tabular_data.txt', 'w')
manf = open('sequences.fasta', 'w')

#Definimos las ER para busquedas.
campo = re.compile('^//')
ID_principal= re.compile('^DBSOURCE\s+REFSEQ:\s+accession\s+(.*)')
gene_name = re.compile('^/locus_tag="(.*)"')
taxa = re.compile('^/db_xref="taxon:(.*)"')
data_basexref = re.compile('^/db_xref="(.*):(.*)"')
seq = re.compile('^[0-9]+\s+(.+)')

#Generamos las variables.
identifier = ''
genename = ''
taxa_id =''
source_db =''
anotation = ''
sequence =''

#Informacion de cortesia para el usuario.

print '\n'+'Ficheros a procesar'+'\n'
print sys.argv[1:]
print '\n'+'Por favor, sea paciente...'
print ''
print '\t'+'...esto va a tardar unos minutos...'
print ''

#Procesado iterativo de los ficheros
for i in sys.argv [1:]:
	print 'Procesando fichero...' + ' '+ i+'\n'
	
	fhandle=open(i, 'r')
	
#Generamos lista para almacenar las bases de datos cruzadas y escribimos encabezado de columnas.	
	lista = []
	filehandle.writelines('\n'+'\n'+'\n' + 'Section_corresponding_to'+ '\t'+ i+'\t'+ 'file'+'\n'+'\n')
	filehandle.writelines('Identifier'+'\t'+'Gene_name'+'\t'+'NCBI_taxa'+'\t'+'DB_Source'+'\t'+'Anotation'+'\n')
	manf.writelines('\n'+'\n'+'\n' + 'Section_corresponding_to'+ '\t'+ i+'\t'+ 'file'+'\n'+'\n')
#Iteramos en cada uno de los ficheros buscando las ER definidas.	
	for line in fhandle.readlines():
		linestriped = line.strip()
		
		if ID_principal.match(linestriped):
			identifier = ID_principal.match(linestriped).group(1)
				
		if gene_name.match(linestriped):
			genename = gene_name.match(linestriped).group(1)
			
		if taxa.match(linestriped):
			taxa_id = taxa.match(linestriped).group(1)
		
		if data_basexref.match(linestriped):
			lista.append(data_basexref.match(linestriped).group(1))
			lista.append(data_basexref.match(linestriped).group(2))
			
		if seq.match(linestriped):
			sequence += seq.match(linestriped).group(1)

 
#Al tener mas de una entrada cruzada de BD x campo iteramos para anadir cada una de ellas.			
		if campo.match (linestriped):
			for n in range(len(lista)):
				if n%2 == 0:
					source_db = lista[n]
					anotation = lista [n+1]
					filehandle.writelines (identifier+'\t'+genename+'\t'+taxa_id+'\t'+source_db+'\t'+anotation+'\n')
					
			sequen = sequence.replace(' ', '')
			manf.writelines('>gb|'+identifier+'|'+genename+'|'+taxa_id+'\n')
			manf.writelines(sequen+'\n'+'\n')
#Borramos, tras cada campo ('//'), los contenedores temporales de informacion.
			lista=[]
			sequence=''
			sequen=''
	print '...se ha terminado de procesar el fichero:'+' '+i+'\n'+'\n'	
	
#Cerramos ficheros
	
	fhandle.close()

filehandle.close()
manf.close()

