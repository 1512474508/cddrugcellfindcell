import sys
import json 
import uuid

cell2mutationfile = "../data/cell2mutation_list.txt"

go2namefile = "../data/goterm2name.txt"
go2genefile = "../data/goterm2genes.txt" 

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
	rlippfile = sys.argv[2]
	outputfile = inputfile.replace('.txt', '.json')
	
	# load information about GO terms
	go2name = load_mapping(go2namefile, 0, 1)
	go2gene = load_mapping(go2genefile, 0, 1)

	# find relevant information for each GO term 
	rlipp = {}
	with open(rlippfile, 'r') as fi:
		for line in fi:
			tokens = line.strip().split('\t')
			rlipp[tokens[0]] = float(tokens[1])

	# sort rlipp scores
	sorted_rlipp = {k: v for k, v in sorted(rlipp.items(), key=lambda item: item[1], reverse=True)}
	
	rlippfile = rlippfile.replace('.txt', '_sorted.txt')
	with open(rlippfile, 'w') as fo:
		for r in sorted_rlipp:
			fo.write("%s\t%s\t%.6f\t%s\n" % (r, go2name[r], sorted_rlipp[r], go2gene[r]))	

	# load mapping between cell to id mapping
	cell2genes = load_mapping(cell2mutationfile, 0, 1)

	# build a dictionary for the results
	output = {}
	output['predictions'] = []

	# collect the top RLIPP pathways	
	top_pathways = []

	with open(rlippfile, 'r') as fi:
		for i in range(top_n):
			line = fi.readline()
			tokens = line.strip().split('\t')

			top_pathways.append({'GO_id': tokens[0], 'pathway_name': tokens[1], 'RLIPP': tokens[2], 'pathway_genes': tokens[3]})

	output['top_pathways'] = top_pathways


	with open(inputfile, 'r') as fi:
		for line in fi:
			tokens = line.strip().split('\t')
	
			cellname = tokens[0]
			smiles = tokens[1]
			predicted = float(tokens[3])
	
			# add a line to .json
			output['predictions'].append({'cell': cellname, 'predicted_AUC': predicted, 'mutations': cell2genes[cellname]})



	with open(outputfile, 'w') as fo:
		json.dump(output, fo, indent=4)
	

if __name__ == "__main__":
	main()
