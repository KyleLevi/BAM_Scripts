import os
import sys
import argparse
import subprocess







if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='', required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


    tmp = args.input + '.tmp'
    with open(tmp, 'w') as tmpfile:
        with open(args.input, 'r') as infile:
            broken = 0
            i = 0
            for line in infile:
                i += 1
                if i == 4 and line.startswith('+'):
                    tmpfile.write(',' + line[1:])
                else:
                    tmpfile.write(line)
    if broken == 0:
        rm_command  = ['rm', tmp]
        ret_code = subprocess.call(rm_command)
        if ret_code != 0:
            sys.stderr.write("Error running command \"{}\"\n".format(' '.join(rm_command)))
            sys.exit(1)
    else:
        mv_command = ['mv', tmp, args.input]
        ret_code = subprocess.call(mv_command)
        if ret_code != 0:
            sys.stderr.write("Error running command \"{}\"\n".format(' '.join(mv_command)))
            sys.exit(1)