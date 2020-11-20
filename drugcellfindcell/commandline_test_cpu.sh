#!/bin/bash
# argument: directory where all the results will be stored

##### pre-processing ##################################################################################
scriptdir=""
outputdir=$1
if [ ! -d "$outputdir" ]
then
	mkdir $outputdir
fi

inputmutationfile=$outputdir"/input_cell2mutation.txt"
inputcell2id=$outputdir"/input_cell2id.txt"
inputfile=$outputdir"/input.txt"

python 1_build_input.py $outputdir/input_genes.txt $outputdir

######################################################################################################


##### run DrugCell prediction #########################################################################
inputdir="/opt/drugcell/DrugCell/data/"
gene2idfile=$inputdir"gene2ind.txt"
drug2idfile=$inputdir"drug2ind.txt"
drugfile=$inputdir"drug2fingerprint.txt"

modelfile="/opt/drugcell/DrugCell/pretrained_model/drugcell_v1.pt"

source activate pytorch3drugcellcpu

python -u /opt/drugcell/DrugCell/code/predict_drugcell_cpu_nohidden.py -gene2id $gene2idfile -cell2id $inputcell2id -drug2id $drug2idfile -genotype $inputmutationfile -fingerprint $drugfile -result $outputdir -predict $inputfile -load $modelfile 

paste -d "\t" <(cat $outputdir/input.txt) <(cat $outputdir/drugcell.predict) > $outputdir/output.txt
rm $outputdir/drugcell.predict

#######################################################################################################


##### map drug names to SMILES and generate .json file ################################################

python 2_generate_output.py $outputdir/output.txt

#######################################################################################################
