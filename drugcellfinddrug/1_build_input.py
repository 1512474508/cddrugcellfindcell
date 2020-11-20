import sys

workingdir = "/opt/drugcell/DrugCell/data/"
gene2idfile = workingdir + "gene2ind.txt"
drug2idfile = workingdir + "drug2ind.txt"

cell_name = "user_cell"

# load one column from a file
def load_1col(filename, ind):
	data = set()
	with open(filename, 'r') as fi:
		for line in fi:
			tokens = line.strip().split('\t')
			data.add(tokens[ind])
	return list(data)


# load mapping from a file
def load_mapping(filename):
	mapping = {}
	with open(filename, 'r') as fi:
		for line in fi:
			tokens = line.strip().split('\t')
			mapping[tokens[1]] = int(tokens[0])
	return mapping


# main function
def main():
	# load data
	gene2id = load_mapping(gene2idfile)
	drugs = load_1col(drug2idfile, 1)

	# load input data
	inputfile = sys.argv[1]
	inputgenes = load_1col(inputfile, 0)

	outputdir = sys.argv[2] + "/"

	# filtered genes - non-DrugCell genes
	new_inputgenes = set(gene2id.keys()).intersection(inputgenes)
	filtered_genes = set(inputgenes).difference(new_inputgenes)

	# log filtered genes
	with open(outputdir + "filtered_genes.txt", 'w') as fo:
		fo.write('\n'.join(list(filtered_genes)))

	# build the genotype of cell
	vec = [0] * len(gene2id)
	for g in new_inputgenes:
		vec[gene2id[g]] = 1

	# print out new genotype input file
	with open(outputdir + "input_cell2mutation.txt", 'w') as fo:
		fo.write("%s\n" % ','.join(list(map(str, vec))))
		fo.write("%s\n" % ','.join(list(map(str, vec))))

	# generate new input cell2ind file
	with open(outputdir + "input_cell2id.txt", 'w') as fo:
		fo.write("0\t%s\n" % cell_name)
		fo.write("1\t%s_dim\n" % cell_name)

	# generate new input data file for prediction
	with open(outputdir + "input.txt", 'w') as fo:
		for d in drugs:
			fo.write("%s\t%s\t-1\n" % (cell_name, d))
	




if __name__ == "__main__":
	main()
