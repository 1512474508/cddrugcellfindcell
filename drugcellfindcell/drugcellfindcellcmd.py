#!/usr/bin/env python

import os
import subprocess
import sys
import argparse
import json
import drugcellfindcell


def _parse_arguments(desc, args):
    """
    Parses command line arguments
    :param desc:
    :param args:
    :return:
    """
    help_fm = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=help_fm)
    parser.add_argument('input',
                        help='comma delimited list of genes in file')
    parser.add_argument('--email',
                        help='e-mail address to notify upon completion')
    return parser.parse_args(args)


def read_inputfile(inputfile):
    """

    :param inputfile:
    :return:
    """
    with open(inputfile, 'r') as f:
        return f.read()


def main(args):
    """
    Main entry point for program

    :param args: command line arguments usually :py:const:`sys.argv`
    :return: 0 for success otherwise failure
    :rtype: int
    """
    desc = """
        Using gprofiler-official 1.0.0, Python module, this
        program takes a file with comma delimited list of genes 
        as input and outputs best matching term in JSON format to
        standard out. Any log messages and errors are output to
        standard error.
        
        Return 0 upon success otherwise error.
        
        Format of JSON output:
        
        {
         "name": "<TERM NAME>",
         "source": "<IS THE NAME FOR THE DATASOURCE>",
         "sourceTermId": "<IS THE ID FOR THE ENRICHED TERM/FUNCTIONAL CATEGORY IN ITS NATIVE NAMESPACE>",
         "p_value": <PVALUE>,
         "jaccard": <JACCARD VALUE>,
         "description": "<DESCRIPTION, IF ANY, FOR TERM>",
         "term_size": <NUMBER OF GENES ASSOCIATED WITH TERM>,
         "intersections": ["<LIST OF GENES USED TO GET TERM>"]
        }

    """

    theargs = _parse_arguments(desc, args[1:])
    taskId = theargs.input[theargs.input.index('/tasks/') + 7 : theargs.input.index('/input.txt')]

    try:
        inputfile = os.path.abspath(theargs.input)
        os.mkdir("/tmp/drugcellinput")

        inputGenes = read_inputfile(inputfile)
        genes = inputGenes.strip(',').strip('\n').split(',')

        f = open("/tmp/drugcellinput/input_genes.txt", "a+")
        for gene in genes:
            f.write(gene + "\n")
        f.close()

        os.chdir("/opt/conda/bin")

        drugcell_pipeline = "commandline_test_cpu.sh"
        drugcell_input_directory = "/tmp/drugcellinput"

        with open('/tmp/drugcellinput/output.log', 'a') as stdout:
            with open('/tmp/drugcellinput/error.log', 'a') as stderr:
                subprocess.call(
                    [drugcell_pipeline, drugcell_input_directory], stdout=stdout, stderr=stderr)

        with open('/tmp/drugcellinput/output.json') as f:
            jsonResult = json.load(f)

        theres = {
            'taskId': taskId,
            'email': theargs.email,
            'inputGenes': inputGenes,
            'predictions': jsonResult['predictions']
        }
        if theres is None:
            sys.stderr.write('No drugs found\n')
        else:
            json.dump(theres, sys.stdout)
        sys.stdout.flush()
        return 0
    except Exception as e:
        sys.stderr.write('Caught exception: ' + str(e))
        return 2


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
