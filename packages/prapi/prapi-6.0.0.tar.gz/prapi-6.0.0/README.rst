=============
Prapi Summary
=============
More Detail information is on http://www.bioinfor.org/tool/PRAPI/.

PRAPI is a one-stop solution for Iso-Seq analysis of analyze alternative transcription initiation (ATI), alternative splicing (AS), alternative cleavage and polyadenylation (APA), natural antisense transcripts (NAT), and circular RNAs (circRNAs) comprehensively. 



============
Installation
============

Basic prapi installation (python 2.7 and 3.4+ support)

::
	##################################
    # Before install,Please install these base.
    ##################################
$conda install -y -c bioconda bx-python
$conda install -y -c bioconda pycairo
$conda install -c bioconda pysam
$conda install -c bioconda gmap
$conda install -c biocodna samtools==0.1.19
$conda install -c bioconda  gmap==2016.09.23
$conda install -c bioconda cufflinks==2.2.1
$conda install -c bioconda bioconductor-edger
$conda install -c bioconda bioconductor-degseq
$pip install scipy
$pip install fisher
$pip install CIRCexplorer
$wget http://www.bioinfor.org/tool/PRAPI/download/SpliceGrapher-0.2.5.tar.gz
$tar -xzvf SpliceGrapher-0.2.5.tar.gz
$cd SpliceGrapher-0.2.5
$python setup.py install
    ################################
    #After this,Please install prapi
$pip install prapi
    ####################################
    #test file 
    wget http://www.bioinfor.org/tool/PRAPI/download/v2/test_v2.tar.gz
    tar -xvzf test_v2.tar.gz
    cd test_v2
    sh run.sh
    ####################################
   See more complete tutorials on the `documentation page <http://www.bioinfor.org/tool/PRAPI/manual.php>`_.

===
RNA
===


=====================
Further Documentation
=====================

========
Citation
========

Gao Y, Wang H, Zhang H, Wang Y, Chen J, Gu L, (2017), PRAPI: post-transcriptional regulation analysis pipeline for Iso-Seq.Bioinformatics,Bioinformatics, btx830,https://doi.org/10.1093/bioinformatics/btx830 
============
