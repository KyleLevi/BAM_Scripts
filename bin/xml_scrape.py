#!/usr/bin/env python3

import os
import sys
import argparse
import urllib.request as ur
import re
from bs4 import BeautifulSoup


def run_to_xml_soup(sra_run_id, save_dir=None):
    """
    Reads in an SRA Run accession and returns the XML metadata file of that run as a BS4 "soup" object
    Also, if a directory is specified in the second argument, the XML file will be read from there if it exists
    or saved to that directory if it does not exist.
    :param sra_run_id: String, EX: 'SRR3403834'
    :param save_dir: String, EX: '~/Desktop/SRA_XML_files/'
    :return: soup (BeautifulSoup4 object, where parser='xml')
    """
    if save_dir:
        if sra_run_id in os.listdir(save_dir):
            with open(save_dir + sra_run_id + '.xml', 'r') as infile:
                html = infile.read()
        else:
            url = "http://www.ncbi.nlm.nih.gov/Traces/sra/?run={}&experimental=1&retmode=xml".format(sra_run_id)
            page = ur.urlopen(url)
            html = page.read()
            page.close()
            with open(save_dir + sra_run_id + '.xml', 'w') as outfile:
                outfile.write(html)
    else:
        url = "http://www.ncbi.nlm.nih.gov/Traces/sra/?run={}&experimental=1&retmode=xml".format(sra_run_id)
        page = ur.urlopen(url)
        html = page.read()
        page.close()
    xml_soup = BeautifulSoup(html, 'xml')
    return xml_soup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This program takes in a run accession (EX: SRR3403834) with -i and reads the associated XML '
                    'metadata file from the web.  If -s is specified, the file will be saved in that directory.'
                    'To get the most out of this program, open it and edit lines 65 onward to suit your needs.')
    parser.add_argument('-i', '--input', help='Input file', required=True)
    parser.add_argument('-o', '--output', help='Output to file instead of standard output')
    parser.add_argument('-k', '--keywords', help='Terms to search for', nargs="*")
    parser.add_argument('-f', '--full', help='Display the full \'pretty\' XML in stdout', action='store_true')
    parser.add_argument('-s', '--save', help='Directory to save downloaded XML files in,'
                                   'Also use this to specify if saved XML files are available to skip downloading')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if not args.save.endswith('/'):
        args.save = args.save + '/'

    if not args.keywords:
        # This is the default if --keywords is not used, change it to suit your own needs!
        args.keywords = ['STUDY_ABSTRACT', 'SCIENTIFIC_NAME', 'STUDY_TITLE']

    soup = run_to_xml_soup(args.input, args.save)

    if args.full:
        sys.stdout.write(soup.prettify())
    # Here is where you can change what is being printed, a few examples are shown below
    #-----------------------------------------------------------------------------------

    # Uncomment the following lines to print all (tag, value) pairs for a run
    #tags = [a.string for a in soup.find_all('TAG')]
    #values = [a.string for a in soup.find_all('VALUE')]
    #tag_values = zip(tags, values)
    #sys.stdout.write(tag_values + '\n')

    # Here is an example of getting a full tag with BS4 and printing it
    #read_stats = soup.findAll('Statistics')
    #sys.stdout.write(read_stats + '\n')

    # This is the same example, but using a regex search
    #string_soup = str(soup)
    #results = re.findall('<Statistics .*?</Statistics>', string_soup)
    #read_stats = str(results)
    #sys.stdout.write(read_stats + '\n')

    # Here is a method for printing all of the arguments taken in with -k or --keywords
    for keyword in args.keywords:
        sys.stdout.write(keyword + '\t' + str(soup.find_all(keyword)) + '\n')


