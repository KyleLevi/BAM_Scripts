BAM_Scripts is a collection of tools grouped into two main functions.
1) Getting publicly available data from the Sequence Read Archive (SRA) and using read mapping (Bowtie2) to search for reads of interest.
2) Analyzing and visualizing data stored in .BAM or .SAM files.

**This project is currently in development** 

This project requires the following:
The [SRA toolkit](https://github.com/ncbi/sra-tools/wiki/HowTo:-Binary-Installation)
\
[Samtools/HTSlib](http://www.htslib.org/download/)
\
Python:
1. Transfer the compression version of the files to your server.

$ wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
2. Decompress the files with the following command:

$ tar xvzf Python-3.6.1.tgz
Note: This will create the directory /home/user-name/Python-3.6.1 and automatically decompress all of Python’s files into their appropriate spots.

3. Go into that directory with:

$ cd Python-3.6.1
4. Once inside that directory, install your new version of Python.

$ ./configure --prefix=$HOME/.local
Note: This step sets up your configuration and makes files.

5. Then run this command:

$ make
6. And follow that up with:

$ make install
The last command will install two of the most useful Python utilities:


pip: Python’s recommended tool for installing Python packages.
setuptools: Enables you to download, build, install, and uninstall Python packages.
Fairly easy, but you’re not done yet. Next, you must add the path to your environment. I use vi, the one true editor, for this but you can use Emacs, nano, or any other pure text editor. Never use a word processor, such as Microsoft Word or LibreOffice Writer. These add formatting codes to their documents, which make them worse than useless for coding purposes.



1. Go into your Bash profile configuration file:

$cd $home
$ nano .bash_profile
2. With an editor, add the following lines, then save the file:

# Python 3 
export PATH="$HOME/.local/bin:$PATH"
3. Run the following to get your environment up to date:

$ source ~/.bash_profile
4. Then run the following from the shell and you should see Python 3.6.1:

$ python3 -V
You now have Python 3 installed. Congratulations!