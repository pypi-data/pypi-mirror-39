# insertcode  
* extension util for insert different code in the different file type

# release notes
* Dec 6th  2018 release 0.0.6 for pythonc subcommand to transfer c language to python string
* Sep 20th 2018 release 0.0.4 for python3 support
* Sep 19th 2018 release 0.0.2 for first use

# HOWTO

## shperl  to insert perl code in bash command
> run_perl.sh.tmpl
```shell
#! /bin/sh

PERL_PRINT_STR="use strict;my (\$cmd)=\"%REPLACE_PATTERN%\";eval \$cmd;"
perl -e "$PERL_PRINT_STR" -- $@
```

> a.pl
```perl
#! /usr/bin/env perl

use strict;
use Cwd "abs_path";
use File::Basename;
use Getopt::Long;
use File::Spec;

sub Usage($$)
{
	my ($ec,$fmt)=@_;
	my ($fp)=\*STDERR;

	if ($ec == 0) {
		$fp =\*STDOUT;
	}

	if (length($fmt) > 0) {
		print $fp "$fmt\n";
	}

	print $fp "$0 [OPTIONS]  [dirs]...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";
	print $fp "\t-v|--verbose            to make verbose mode\n";
	print $fp "\n";
	print $fp "\t[dirs]                  if will give basename of it\n";

	exit($ec);
}

my $logo="basename";


use Cwd "abs_path";
use File::Basename;
use File::Spec;


my ($verbose)=0;

sub Debug($)
{
	my ($fmt)=@_;
	my ($fmtstr)="$logo ";
	if ($verbose > 0) {
		if ($verbose >= 3) {
			my ($p,$f,$l) = caller;
			$fmtstr .= "[$f:$l] ";
		}
		$fmtstr .= $fmt;
		print STDERR "$fmtstr\n";
	}
}

sub Error($)
{
	my ($fmt)=@_;
	my ($fmtstr)="$logo ";
	if ($verbose >= 3) {
		my ($p,$f,$l) = caller;
		$fmtstr .= "[$f:$l] ";
	}
	$fmtstr .= $fmt;
	print STDERR "$fmtstr\n";
}

sub FinalOutput($)
{
	my ($output) = @_;
	if ($output && -t STDOUT) {
		print "\n";
	}
}

sub GetFullPath($)
{
	my ($c) =@_;
	if ( -e $c && !( -l $c) ) {
		return abs_path($c);
	}
	return File::Spec->rel2abs($c);
}

sub TrimRoot($)
{
	my ($c) = @_;
	my $curch;
	while (length($c) > 0 ) {
		$curch = substr($c,0,1);
		if ($curch eq "/" ||
			$curch eq "\\") {
			$c =~ s/.//;
		} else {
			last;
		}
	}
	return $c;
}

sub format_out($$$@)
{
	my ($simple,$hashref,$notice,@vals)=@_;
	my ($outstr)="";
	my (@arr);
	foreach (@vals) {
		my ($curval) = $_;
		if (defined($hashref->{$curval})) {
			if ($simple) {
				if (ref ($hashref->{$curval}) eq "ARRAY") {
					@arr = @{$hashref->{$curval}};
					foreach (@arr) {
						$outstr .= "$_\n";	
					}
				} else{
					$outstr .= $hashref->{$curval}."\n";
				}
			} else {
				if (ref ($hashref->{$curval}) eq "ARRAY") {
					@arr = @{$hashref->{$curval}};
					foreach (@arr) {
						$outstr .= "$_ $curval $notice\n";
					}
				} else {
					$outstr .= $hashref->{$curval}." $curval $notice\n";
				}
			}
		}
	}
	return $outstr;
}

sub trimspace($)
{
	my ($retl)=@_;
	$retl =~ s/^\s+//;
	$retl =~ s/\s+$//;
	return $retl;
}


my %opts;
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		${opts{"verbose"}} ++;
	});

if (defined($opts{"help"})) {
	Usage(0,"");
}

if (defined($opts{"verbose"})) {
	$verbose = $opts{"verbose"};
}

foreach(@ARGV) {
	my ($c) = $_;
	$c = GetFullPath($c);
	Debug("[$c]");
	print basename($c)."\n";
}
```

> run change
```shell
python -m insertcode shperl -i run_perl.sh.tmpl -o run_perl.sh  -p '%REPLACE_PATTERN%' a.pl
```
> get the run_perl.sh
> you can call the equivalent function with perl like
```shell
./run_perl.sh -h
```

## shpython to insert python code in bash command
> run_python.sh.tmpl
```shell
#! /bin/sh

PYTHON_PRINT_STR="import sys;cmd='%REPLACE_PATTERN%';exec('%s'%(cmd));"
python -c "$PYTHON_PRINT_STR"  $@
```

> diffdir.py
```python
#! /usr/bin/env python

import extargsparse
import sys
import logging
import os

class CheckFiles(object):
	def __init__(self,crignore=True):
		self.only = []
		self.diffs = []
		self.crignore = crignore
		return

	def check_file_same(self,leftfile,rightfile):
		llines = []
		logging.info('leftfile [%s] rightfile [%s]'%(leftfile,rightfile))
		with open(leftfile,'rb') as f:
			for l in f:
				llines.append(l)
		rlines = []
		with open(rightfile,'rb') as f:
			for l in f:
				rlines.append(l)

		if len(llines) != len(rlines):
			logging.warn('[%s] (%d) != [%s] (%d)'%(leftfile,len(llines),rightfile,len(rlines)))
			return False

		i = 0
		while i < len(llines):
			ll = llines[i]
			rl = rlines[i]
			if rl != ll:
				if not self.crignore:
					diffcnt = 0
					while diffcnt < len(ll) or diffcnt < len(rl):
						if ll[diffcnt] != rl[diffcnt]:
							break
						diffcnt = diffcnt + 1
					s = '[%d]([%s]<>[%s]) at offset[%d] (0x%02x) <> (0x%02x)\n'%(i,leftfile,rightfile,diffcnt,ord(ll[diffcnt]),ord(rl[diffcnt]))
					s += 'from >>>>>>>>>>>>>>>>\n'
					s += '%s'%(ll)
					s += 'to <<<<<<<<<<<<<<<<<<<\n'
					s += '%s'%(rl)
					if self.crignore:
						logging.warn('%s'%(s))
					else:
						logging.debug('%s'%(s))
					return False
				ll = ll.replace('\r','')
				rl = rl.replace('\r','')
				if ll != rl:
					diffcnt = 0
					while diffcnt < len(ll) or diffcnt < len(rl):
						if ll[diffcnt] != rl[diffcnt]:
							break
						diffcnt = diffcnt + 1
					s = '[%d]([%s]<>[%s]) at offset[%d] (0x%02x) <> (0x%02x)\n'%(i,leftfile,rightfile,diffcnt,ord(ll[diffcnt]),ord(rl[diffcnt]))
					s += 'from >>>>>>>>>>>>>>>>\n'
					s += '%s'%(ll)
					s += 'to <<<<<<<<<<<<<<<<<<<\n'
					s += '%s'%(rl)
					if self.crignore:
						logging.warn('%s'%(s))
					else:
						logging.debug('%s'%(s))
					return False
			i = i + 1
		return True


	def __format(self):
		s = ''
		s += 'only %s diffs %s'%(self.only, self.diffs)
		return s

	def __str__(self):
		return self.__format()

	def __repr__(self):
		return self.__format()


class CompoundCheckFiles(CheckFiles):
	def __init__(self,crignore=True):
		super(CompoundCheckFiles,self).__init__(crignore)
		self.left_diffs = []
		self.right_diffs = []
		self.left_only = []
		self.right_only = []
		return

	def __format(self):
		s = ''
		s += 'left_only [%d] [%s]\n'%(len(self.left_only),self.left_only)
		s += 'left_diffs [%d] [%s]\n'%(len(self.left_diffs),self.left_diffs)
		s += 'right_only [%d] [%s]\n'%(len(self.right_only),self.right_only)
		s += 'right_diffs [%d] [%s]\n'%(len(self.right_diffs),self.right_diffs)
		return s

	def __str__(self):
		return self.__format()

	def __repr__(self):
		return self.__format()

class DiffDir(object):
	def __init__(self):
		return

	def __compare_dir(self,fromdir,todir,crignore=True):
		cfs = CheckFiles(crignore)
		for root, dirs,files in os.walk(fromdir):
			if root == fromdir  or root == os.path.join(fromdir,os.pathsep):
				npart = ''
			else:
				npart = os.path.relpath(root,fromdir)
			logging.info('npart %s root %s'%(npart, root))
			logging.info('dirs %s'%(dirs))
			logging.info('files %s'%(files))
			for d in dirs:
				nd = os.path.join(npart,d)
				nfdir = os.path.join(root,d)
				ntdir = os.path.join(todir,npart,d)
				if not os.path.exists(ntdir):
					if nd not in cfs.only:
						cfs.only.append(nd)
					continue
			for f in files:
				nf = os.path.join(npart,f)
				nffile = os.path.join(root,f)
				ntfile = os.path.join(todir,npart,f)
				if not os.path.exists(ntfile):
					if nf not in cfs.only:
						cfs.only.append(nf)
					continue
				# now we should check whether
				if (os.path.islink(ntfile) and not (os.path.islink(nffile))) or (not os.path.islink(ntfile) and (os.path.islink(nffile))):
					if nf not in cfs.diffs:
						cfs.diffs.append(nf)
					continue

				retval = cfs.check_file_same(nffile,ntfile)	
				if not retval:
					if nf not in cfs.diffs:
						cfs.diffs.append(nf)
		return cfs

	def dircompare(self,fromdir,todir,crignore=True):
		compound = CompoundCheckFiles(crignore)
		cfs = self.__compare_dir(fromdir, todir,crignore)
		for d in cfs.diffs:
			nd = os.path.join(fromdir,d)
			if nd not in compound.left_diffs:
				logging.debug('left_diffs append [%s]'%(nd))
				compound.left_diffs.append(nd)
		for d in cfs.only:
			nd = os.path.join(fromdir,d)
			if nd not in compound.left_only:
				logging.debug('left_only append [%s]'%(nd))
				compound.left_only.append(nd)

		cfs = self.__compare_dir(todir,fromdir,crignore)
		for d in cfs.diffs:
			nd = os.path.join(todir,d)
			if nd not in compound.right_diffs:
				logging.debug('right_diffs append [%s]'%(nd))
				compound.right_diffs.append(nd)
		for d in cfs.only:
			nd = os.path.join(todir,d)
			if nd not in compound.right_only:
				logging.debug('right_only append [%s]'%(nd))
				compound.right_only.append(nd)
		return compound

def set_log_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    elif args.verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    if logging.root and logging.root.handlers :
    	logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return


def main():
	commandline='''
	{
		"verbose|v" : "+"
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line()
	set_log_level(args)
	i = 0
	argc = len(args.args)
	d = DiffDir()
	while i < (argc -1):
		cfs = d.dircompare(args.args[i], args.args[i+1])
		logging.info('cfs %s'%(repr(cfs)))
		i += 2
	return

main()
```

> to make the shell code
```shell
python -m insertcode -i run_python.sh.tmpl -o run_python.sh -p '%REPLACE_PATTERN%' shpython diffdir.py
```

> will run as the python call function
```shell
./run_python.sh -h
```
> like
```
python diffdir.py -h
```

## bashstring     to insert the bash string in the bash
> echocode.tmpl
```shell
#! /bin/bash

read -r -d '' CODE<<CODEOF
%REPLACE_PATTERN%
CODEOF

echo -n "$CODE"
```

> a.sh
```shell
#! /usr/bin/env bash

echo -en "hello \n\tworld\r\n"
```

> run format
```shell
python -m insertcode -i echocode.tmpl -o echocode bashstring -p '%REPLACE_PATTERN%' a.sh
```

> to run shell file
```shell
./echocode
```

> it will display the code of a.sh  it is useful when call some shell

## makepython     to insert python code into make file
> run_python.mak.tmpl
```make

define COPY_TO
$(shell python -c "import sys;c='%REPLACE_PATTERN%';exec(c);" $(1) $(2))
endef

all:cpto.py.tmpl

cpto.py.tmpl:cpto.py
	$(call COPY_TO, $<,$@)

clean:
	rm -f cpto.py.tmpl
```

## makeperl   to insert perl code into makefile
> run_perl.mak.tmpl
```make
define COPY_TO
$(shell perl -e "use strict;my (\$$cmd)=\"%REPLACE_PATTERN%\";eval \$$cmd;" --  "$(1)" "$(2)" )
endef

all:cpto.pl.tmpl

cpto.pl.tmpl:cpto.pl
	$(call COPY_TO, $<,$@)

clean:
	rm -f cpto.pl.tmpl

```
> cpto.pl
```perl
#! /usr/bin/env perl

use strict;
use warnings;

if (scalar(@ARGV) >= 2) {
	my ($f) = shift @ARGV;
	my ($t) = shift @ARGV;
	my ($cmd) = "cp -f $f $t";
	system($cmd);
}
```

> run insert code
```shell
python -m insertcode makeperl -i run_perl.mak.tmpl -o run_perl.mak makepython -p '%REPLACE_PATTERN%' cpto.pl
```

> format run_perl.mak
```shell
make -f run_perl.mak all
```

## c insert into python
> hello.c
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc,char* argv[])
{
	printf("hello world\n");
	return 0;
}
```


> echoc.py.tmpl
```python
#! /usr/bin/env python

import sys

LONG_C_FILE='''%REPLACE_PATTERN%'''


def main():
	sys.stdout.write('%s'%(LONG_C_FILE))
	return

if __name__ == '__main__':
	main()
```

> run shell
```shell
python -m insertcode pythonc -i echoc.py.tmpl -o echoc.py -p '%REPLACE_PATTERN%' hello.c
```

> run new python file echoc.py will output hello.c file content