========================
Representatives database
========================

In order to do read-level taxonomic binning, representative databases need to be compiled. Four default databases were designed cover most of the genetic diversities in metagenomic samples. 

**ANI 98% database for bacteria and archaea**

.. code-block:: bash

    sparse query --dbname refseq --default representative | python SPARSE.py mapDB --dbname refseq --seqlist stdin --mapDB representative

**ANI 99% database for bacteria and archaea (always use together with representative database)**

.. code-block:: bash

    sparse query --dbname refseq --default subpopulation | python SPARSE.py mapDB --dbname refseq --seqlist stdin --mapDB subpopulation

**ANI 99% virus database**

.. code-block:: bash

    sparse query --dbname refseq --default Virus | python SPARSE.py mapDB --dbname refseq --seqlist stdin --mapDB Virus

**ANI 99% eukaryota database (genome size <= 200MB)**

.. code-block:: bash

   sparse query --dbname refseq --default Eukaryota | python SPARSE.py mapDB --dbname refseq --seqlist stdin --mapDB Eukaryota

**Custom databases** 

In order to index a differet set of references into a representative database, see [here](custom.md)
