import sys
import json 
import uuid

drug2idfile = "/opt/drugcell/DrugCell/data/drug2ind.txt"
drugmappingfile = "/opt/drugcell/DrugCell/data/compound_names.txt" 

rlippfile_prefix = "/opt/drugcell/DrugCell/data/rlipp/fallmo100_rlipp_"
top_n = 10

# load mapping from a file
def load_mapping(filename, keyind, valind, skipline=0):
	mapping = {}
	with open(filename, 'r') as fi:
		if skipline > 0:
			for i in range(skipline):
				fi.readline()

		for line in fi:
			tokens = line.strip().split('\t')
			mapping[tokens[keyind]] = tokens[valind]
	return mapping



def main():
	inputfile = sys.argv[1]
	outputfile = inputfile.replace('.txt', '.json')
	
	# load mapping between smiles to drug id
	smiles2id = load_mapping(drug2idfile, 1, 0)

	# load mapping between smiles and drug names
	smiles2name = load_mapping(drugmappingfile, 1, 2, 1)

	# generate uuid for this instance
	this_id = str(uuid.uuid1())

	# build a dictionary for the results
	output = {}
	output['predictions'] = []

	# read output of DrugCell and add drug name
	inputfile = sys.argv[1]
	outputfile = inputfile.replace('.txt', '.json')

	with open(inputfile, 'r') as fi:
		for line in fi:
			tokens = line.strip().split('\t')
	
			smiles = tokens[1]
			drug_id = smiles2id[smiles]
			predicted = float(tokens[3])

			drug_name = "unknown" 
			try:
				drug_name = smiles2name[smiles]
			except:
				pass
		
			# collect the top RLIPP pathways	
			rlipp_file = rlippfile_prefix + drug_id + ".names"
			top_pathways = []
	
			with open(rlipp_file, 'r') as fi:
				for i in range(top_n):
					line = fi.readline()
					tokens = line.strip().split('\t')
					top_pathways.append({'GO_id': tokens[1], 'pathway_name': tokens[4], 'RLIPP': float(tokens[3])})
	
			# add a line to .json
			output['predictions'].append({'drug_id': drug_id, 'drug_name': drug_name, 'predicted_AUC': predicted, 'drug_smiles': smiles, 'top_pathways': top_pathways})

	with open(outputfile, 'w') as fo:
		json.dump(output, fo, indent=4)
	

if __name__ == "__main__":
	main()
