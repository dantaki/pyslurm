# pyslurm
construct SLURM job submission scripts

```
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
	 
```
