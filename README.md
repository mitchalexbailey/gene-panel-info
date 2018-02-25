# gene-panel-info
## Overview
Combines information from multiple publicly available sources (Orphanet, Gene Ontology [GO] Cosortium) to facilitate a better understanding of which genes and what conditions are included on epilepsy gene panels.

## Data Sources
* Orphadata (Accessed January 31, 2018): http://www.orphadata.org
  * en_product6.xml: Disorders and their associated genes
  * en_product1.xml: Disorders, cross referenced with other nomenclatures
* Gene Ontology Consortium (GO) MySQL Database: http://www.geneontology.org/page/go-mysql-database-guide
 

## Use
From comma-separated list of gene symbols, the GO database and Orphadata files will be searched and output will be either printed or written to specified file (default: "gene-panel-info_[dash-separated list of gene symbols].txt").
* Output file can be specified with -o flag (example 2).
* Output will be printed as well as written to file with -p flag (example 3)

Example 1: Output written to "gene-panel-info_TP53-RB1-PTEN.txt":

`python gene-panel-info.py "TP53, RB1, PTEN"`

Example 2: Output written to "tumor_supressor-info.txt":

`python gene-panel-info.py "TP53, RB1, PTEN" -o "tumor_supressor-info.txt"`

Example 3: Output printed and written to "tumor_supressor-info.txt":

`python gene-panel-info.py "TP53, RB1, PTEN" -o "tumor_supressor-info.txt" -p`


## References
* Ashburner et al. Gene ontology: tool for the unification of biology (2000) Nat Genet 25(1):25-9. Online at Nature Genetics.

* GO Consortium, Nucleic Acids Res., 2017

* Orphadata: Free access data from Orphanet. © INSERM 1997. Available on http://www.orphadata.org. XML data version.
