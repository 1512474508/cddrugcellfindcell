import sys
from rdkit import Chem
from rdkit.Chem.Draw import SimilarityMaps


cell2idfile = "../data/cell2ind.txt"

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
	cells = load_1col(cell2idfile, 1)

	# load input data
	inputfile = sys.argv[1]
	inputdrug = load_1col(inputfile, 0)[0]

	outputdir = sys.argv[2] + "/"

	# build morgan fingerprint for the input drug
	d = Chem.MolFromSmiles(inputdrug)
	f = list(map(str, list(SimilarityMaps.GetMorganFingerprint(d, fpType='bv',radius=2))))

	# print out new genotype input file
	with open(outputdir + "input_drug_fingerprint.txt", 'w') as fo:
		fo.write("%s\n" % ','.join(f))
		fo.write("%s\n" % ','.join(f))

	# generate new input cell2ind file
	with open(outputdir + "input_drug2id.txt", 'w') as fo:
		fo.write("0\t%s\n" % inputdrug)
		fo.write("1\tdummy_%s\n" % inputdrug)

	# generate new input data file for prediction
	with open(outputdir + "input.txt", 'w') as fo:
		for c in cells:
			fo.write("%s\t%s\t-1\n" % (c, inputdrug))
	


if __name__ == "__main__":
	main()
