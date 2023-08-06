========================================
Building custom representative databases
========================================
You can also custom the representative databases. Here a human genome is used as an example:

**We first query its record in a SPARSE refseq database using the assembly accession:**

.. code-block:: bash

    sparse query --dbname refseq_20171014 --assembly_accession GCF_000001405.37 > human.tsv

**The resulting file is:**

.. code-block:: bash

    index	deleted barcode sha256	size	assembly_accession	version refseq_category assembly_level	taxid	organism_name	file_path	url_path	subspecies	species genus	family	order	class	phylum	kingdom superkingdom

    107460	-	u107460.s107460.r107460.p107460.n107460.m107460.e107460.c107460.a107460 d236b7835a3f10e596f9ce3c1f988b9e897f2dea216fd3dcde880eb91963863e	3253848404	GCF_000001405.37	37	reference genome	Chromosome	9606	Homo sapiens	-	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.37_GRCh38.p11/GCF_000001405.37_GRCh38.p11_genomic.fna.gz	-	Homo sapiens	Homo	Hominidae	Primates	Mammalia	Chordata	Metazoa	Eukaryota

**This file can be used as an input to build a new representative database named "Human":**

.. code-block:: bash

    sparse mapDB --dbname refseq --mapDB Human --seqlist human.tsv


Metagenomic reads are assigned using these representative databases, details see section on  "read-level prediction".

