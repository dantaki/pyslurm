#!/usr/bin/env python
'''
Copyright <2018> <Danny Antaki>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from argparse import RawTextHelpFormatter
import argparse,os,sys
__version__='0.0.1'
__usage__="""

██████╗ ██╗   ██╗███████╗██╗     ██╗   ██╗██████╗ ███╗   ███╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║     ██║   ██║██╔══██╗████╗ ████║
██████╔╝ ╚████╔╝ ███████╗██║     ██║   ██║██████╔╝██╔████╔██║
██╔═══╝   ╚██╔╝  ╚════██║██║     ██║   ██║██╔══██╗██║╚██╔╝██║
██║        ██║   ███████║███████╗╚██████╔╝██║  ██║██║ ╚═╝ ██║
╚═╝        ╚═╝   ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝
                                                             
        construct SLURM job submission scripts 
------------------------------------------------------------
Version {}
Author: Danny Antaki dantaki at ucsd dot edu

  pyslurm  -i <command> -a <account> -p <partition> 
           -c <cpu>     -t <walltime> -n <jobname> 
           -o <logdir>  -T <array arg> -B <n_parallel>
	
slurm arguments:
  
  -i        file containing commands
  -a        account id
  -p        partition [default: shared]
  -c        cpus [default: 1]
  -t        walltime [D-HH:MM default: 0-08:00]
  -n        job name [default: foo]
  -o        stdout and stderr output directory [default: cwd]

job array arguments:
  -T        array argument [LINE_START-LINE_END]
  -B        parallel jobs

optional arguments:

  -rc       bashrc file to source
  -h        show this message and exit
	 
""".format(__version__)
def header(acct,part,cpu,wall,jobid,err,out):
	a = [
		'#!/bin/bash',
		'#SBATCH --account={}'.format(acct),
		'#SBATCH --partition={}'.format(part),
		'#SBATCH -c {}'.format(cpu),
		'#SBATCH -t {}'.format(wall),
		'#SBATCH --job-name={}'.format(jobid),
		'#SBATCH -o {}'.format(out),
		'#SBATCH -e {}'.format(err),
	]
	return a
def check_walltime(s):
	days = s.split('-')
	if len(days) != 2: 
		sys.stderr.write('ERROR {} MUST BE FORMATTED D-HH:MM\n'.format(s))
		sys.exit(1)
	if days[0] != '0' and days[0] != '1' and days[0] != '2':
		sys.stderr.write('ERROR {} CANNOT BE GREATER THAN 2\n'.format(days[0]))
		sys.exit(1)
	hours = days[1].split(':')
	if len(hours) != 2:
		sys.stderr.write('ERROR {} MUST BE FORMATTED D-HH:MM\n'.format(s))
	if days[0]=='0' and days[1]=='00:00':
		sys.stderr.write('ERROR WALL TIME MUST BE GREATER THAN 0-00:00\n')
		sys.exit(1)
def main():
	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, usage=__usage__, add_help=False)
	slurm_args, array_args, opt_args = parser.add_argument_group('slurm arguments'), parser.add_argument_group('job array arguments'), parser.add_argument_group('optional arguments')
	slurm_args.add_argument('-i',type=str,default=None,required=True)
	slurm_args.add_argument('-a',type=str,default=None,required=True)
	slurm_args.add_argument('-p',type=str,default='shared',required=False)
	slurm_args.add_argument('-c',type=int,default=1,required=False)
	slurm_args.add_argument('-t',type=str,default='0-08:00',required=False)
	slurm_args.add_argument('-n',type=str,default='foo',required=False)
	slurm_args.add_argument('-o',type=str,default=os.getcwd(),required=False)
	array_args.add_argument('-T',type=str,default=None,required=False)
	array_args.add_argument('-B',type=int,default=None,required=False)
	opt_args.add_argument('-rc',type=str,required=False,default=None)
	opt_args.add_argument('-h', '-help', required=False, action="store_true", default=False)
	args = parser.parse_args()
	cmd, acct, part, cpu, wall, jobid, odir = args.i, args.a, args.p, args.c, args.t, args.n, args.o
	arr, arrby = args.T, args.B
	rc, _help = args.rc, args.h
	if (_help==True or len(sys.argv)==1):
		print(__usage__)
		sys.exit(0)
	if not os.path.isfile(cmd): 
		sys.stderr.write('ERROR {} NOT A FILE\n'.format(cmd))
		sys.exit(1)
	if cpu < 0: 
		sys.stderr.write('ERROR {} CAN NOT BE LESS THAN 0\n'.format(cpu))
		sys.exit(1)
	check_walltime(wall)
	if rc != None and not os.path.isfile(rc): 
		sys.stderr.write('ERROR {} NOT A FILE\n'.format(rc))
		sys.exit(1)
	if not odir.endswith('/'): odir=odir+'/'
	err,out = None,None
	if arr==None: 
		err,out = odir+jobid+'_err', odir+jobid+'_out'
		head = header(acct,part,cpu,wall,jobid,err,out)
		_cmd=[]
		with open(cmd,'r') as f: _cmd = [l.rstrip() for l in f]
		sys.stdout.write('{}\n'.format('\n'.join(head)))
		if rc != None: sys.stdout.write('source {}\n'.format(rc))
		sys.stdout.write('{}\n'.format('\n'.join(_cmd)))
	else: 
		err,out = odir+jobid+'_%a_err', odir+jobid+'_%a_out'
		head = header(acct,part,cpu,wall,jobid,err,out)
		sys.stdout.write('{}\n'.format('\n'.join(head)))
		sys.stdout.write('#SBATCH --array={}%{}\n'.format(arr,arrby))
		if rc != None: sys.stdout.write('source {}\n'.format(rc))
		sys.stdout.write('SEED=$(cat {} | head -n $SLURM_ARRAY_TASK_ID | tail -n 1 | awk "{{print $1}}")\n$SEED\n'.format(cmd))
