import os
import sys
import argparse
import urllib
from bs4 import BeautifulSoup


def run_to_xml_soup(sra_run_id, save_dir=None):
    if save_dir:
        if sra_run_id in os.listdir(save_dir):
            with open(save_dir + sra_run_id, 'r') as infile:
                html = infile.read()
        else:
            url = "http://www.ncbi.nlm.nih.gov/Traces/sra/?run={}&experimental=1&retmode=xml".format(sra_run_id)
            page = urllib.urlopen(url)
            html = page.read()
            page.close()
            with open(save_dir + sra_run_id, 'w') as outfile:
                outfile.write(html)
    else:
        url = "http://www.ncbi.nlm.nih.gov/Traces/sra/?run={}&experimental=1&retmode=xml".format(sra_run_id)
        page = urllib.urlopen(url)
        html = page.read()
        page.close()
    soup = BeautifulSoup(html, 'xml')
    return soup

'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('-i', help='Input file', required=True)
    parser.add_argument('-o', help='Output to file instead of standard output')
    parser.add_argument('-k', help='', nargs="*")
    parser.add_argument('-a', help='Display all possible search tags', action='store_true')

    parser.add_argument('-s', help='Directory to save downloaded XML files in,'
                                   'Also use this to specify if saved XML files are available to skip downloading')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
'''
save_dir = '../Input/xml_metadata/'
soup = run_to_xml_soup('srr3403834', save_dir)
print soup.prettify()

'''
argsk = ['DB', 'SCIENTIFIC_NAME', 'TAG', 'VALUE', 'XREF_LINK']
tags = [a.string for a in soup.find_all('TAG')]
values = [a.string for a in soup.find_all('VALUE')]
tag_values = zip(tags, values)
print tag_values
for tag in kargs:
    print tag, [a.string for a in soup.find_all(tag)]
'''

