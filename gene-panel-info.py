#match genes to condition names and OMIM IDs
import argparse
import xml.etree.ElementTree as ET
import json
import pymysql.cursors
from collections import Counter
import operator

def get_gene_ids(gene, cur):
	q = "select id from gene_product where symbol='%s' and species_id='464824';" % gene
	cur.execute(q)
	temp = cur.fetchall()
	unique = []
	for item in temp:
		if item not in unique:
			unique += [item]
		else:
			pass
	clean = []
	try:
		for item in unique:
			clean += [item[0]]
	except:
		clean = unique
	return clean


def get_term_ids(gids, cur):
	tids = []
	for item in gids:
		q = "select term_id from association where gene_product_id='%s';" % item
		cur.execute(q)
		hold = cur.fetchall()
		for item in hold:
			if item not in tids:
				tids += [item]
	i =0 
	try:
		while i < len(tids):
			tids[i] = tids[i][0]
			i += 1
	except:
		pass
	return tids

def get_terms(tids, cur):
	ters = []
	for item in tids:
		q = "select name from term where id = '%s'" % item
		cur.execute(q)
		hold = cur.fetchall()
		for res in hold:
			ters += [res]
	i =0 
	try:
		while i < len(ters):
			ters[i] = ters[i][0]
			i += 1
	except:
		pass
	return ters


parser = argparse.ArgumentParser(description='Retrieve information on the genes provided: Associated locus IDs, phenotypes, GO terms.')
parser.add_argument('genes', type=str, nargs='+',
                    help='Accepts comma-separated list of genes.')
args = parser.parse_args()


temp_genes = args.genes[0]
gene_list = temp_genes.replace(" ","").split(",")

conditions = []
omim_locusids = []
omim_phenids = []
inheritance = []

#instead of repeating sql querys
connection = pymysql.connect(host='spitz.lbl.gov',
                             user='go_select',
                             db='go_latest_lite')
cursor = connection.cursor()

go_terms = []
i=0
while i < len(gene_list):
	gene_ids = get_gene_ids(gene_list[i], cursor)
	term_ids = get_term_ids(gene_ids, cursor)
	temp_terms = get_terms(term_ids, cursor)
	go_terms += [temp_terms]
	i += 1

tree = ET.parse("en_product6.xml")
root = tree.getroot()
dat = root[0]

i = 0
while i < len(gene_list):
	temp_conditions = []
	temp_omim_locusids = []
	for item in dat:
		for subitem in item[3]:
			if subitem[0][2].text == gene_list[i]:
				temp_conditions += [item[1].text]
				for subitem2 in subitem[0][4]:
					if subitem2[0].text == "OMIM":
						temp_omim_locusids += [subitem2[1].text]
					else:
						pass
			else:
				pass
	conditions += [temp_conditions]
	omim_locusids += [temp_omim_locusids]
	i += 1

uq = []
for item in omim_locusids:
	if item not in uq:
		uq += item
	else:
		pass
omim_locusids = uq


del tree
del root
del dat

tree = ET.parse("en_product1.xml")
root = tree.getroot()
dat = root[0]

i = 0
while i < len(conditions):
	temp_omim_phenids = []
	if len(conditions[i]) == 0:
		temp_omim_phenids += ["NA"]
	elif len(conditions[i]) == 1:
		for item in dat:
			if dat[2].text == conditions[i]:
				for subitem in item[6]:
					if subitem[0].text == "OMIM":
						temp_omim_phenids += [subitem[1].text]
	else:
		for item in conditions[i]:
			for refitem in dat:
				if refitem[2].text == item:
					for ref in refitem[6]:
						if ref[0].text == "OMIM":
							temp_omim_phenids += [ref[1].text]
						else:
							pass
				else:
					pass
	omim_phenids += [temp_omim_phenids]
	i += 1


res = {}
i = 0 
while i < len(gene_list):
	res[gene_list[i]] = ({'conditions': conditions[i], 'omim_locusids': omim_locusids[i], 'omim_phenids': omim_phenids[i], 'go_terms': go_terms[i]})
	i += 1

f = open("test.txt", "w")
f.write(json.dumps(res))
f.close() 