#!/bin/bash
# argument: directory where all the results will be stored

##### pre-processing ##################################################################################
scriptdir="/cellar/users/jpark/Data2/DrugCell_web/case3_drug/script/"
outputdir=$1
if [ ! -d "$outputdir" ]
then
	mkdir $outputdir
fi

# rdkit-env can be set up: conda create -c rdkit -n rdkit-env rdkit
source activate rdkit-env
python $scriptdir/1_build_input.py $outputdir/input_drug.txt $outputdir
conda deactivate

inputdrugfile=$outputdir"/input_drug_fingerprint.txt"
inputdrug2id=$outputdir"/input_drug2id.txt"
inputfile=$outputdir"/input.txt"

######################################################################################################


##### run DrugCell prediction #########################################################################
inputdir="/cellar/users/jpark/Data2/DrugCell_web/case3_drug/data/"
gene2idfile=$inputdir"gene2ind.txt"
cell2idfile=$inputdir"cell2ind.txt"
cellmutationfile=$inputdir"cell2mutation.txt"

modelfile=$inputdir"pretrained_model/drugcell_v1.pt"

# create a folder to hidden values 
hiddendir=$outputdir/Hidden
mkdir $hiddendir

# load the necessary conda environment
source activate pytorch3drugcell

python -u $scriptdir/code/predict_drugcell.py -gene2id $gene2idfile -cell2id $cell2idfile -drug2id $inputdrug2id -genotype $cellmutationfile -fingerprint $inputdrugfile -hidden $hiddendir -result $outputdir -predict $inputfile -load $modelfile -cuda 0 

paste -d "\t" <(cat $outputdir/input.txt) <(cat $outputdir/drugcell.predict) > $outputdir/output.txt
rm $outputdir/drugcell.predict

#######################################################################################################


##### map drug names to SMILES and generate .json file ################################################

#python $scriptdir/2_generate_output.py $outputdir/output.txt

#######################################################################################################
