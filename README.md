
# PC-lint Plus + Juliet Test Suite

PC-lint Plus - Static Code Analysis Tool for C and C++ Source Code  
Juliet - C/C++ Software Assurance Reference Dataset

- Executing static code analysis of the Juliet Test Suite using PC-lint.

## True-Positive vs False-Positive

- **false positive** - the error in binary classification in which a test result incorrectly indicates the presence of a condition (such as a disease when the disease is not present). 
- **false negative** - the opposite error, where the test result incorrectly indicates the absence of a condition when it is actually present. 
- **true positive** - the correct result, where the test result correctly indicates the presence of a condition.
- **true negative** - the correct result, where the test result correctly indicates the absence of a condition.

In our case we have:
- **true positive** - when a issue is correctly found in bad-function code.
- **false positive** - when a issue is incorrectly found in good-function code

## Prerequisites

### Install PC-lint Plus

Download *pclp.linux.2.2.tar.gz* from https://pclintplus.com/downloads/

Create the ~pclint directory: `$ mkdir ~/pclint`

Move to the ~pclint directory: `$ cd ~/pclint`

Copy downloaded *pclp.linux.2.2.tar.gz* to ~/pclint

Extract *pclp.linux.2.2.tar.gz* `$ tar -xvzf pclp.linux.2.2.tar.gz`

Copy the license file (* .lic) to: ~/pclint/pclp/

Add pclint to the PATH environment variable, modify: ~/.profile, append the following line at the end:

    PATH="$PATH:$HOME/pclint/pclp"

Log out, log in, check if the pclint is found: `$ which pclp64_linux`

### Install PC-lint required python modules

Assumption that python3 is already installed.

Install PIP (if not already installed):

```bash
sudo apt update
sudo apt install python3-pip
```

Check if successfully installed: `$ pip3 --version`

Install the required python modules regex and pyyaml for PClint to work:

```bash
pip3 install regex
pip3 install pyyaml
```

In case the above gives PEP 668 error message:

```bash
igor@ubuntig:~$ pip3 install regex
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

Install the required python modules regex and pyyaml using 'apt install python3-...'

```bash
sudo apt install python3-regex
sudo apt install python3-yaml
```

### Build imposter with gcc

```bash
cd ~/pclint/pclp/config
gcc imposter.c -o imposter
```

## Prepare pclp_juliet_a

### Copy 

## Excute ig1.sh bash-script

```bash
./ig1.sh <directory_to_analyze>
```

The script will look and load the file args.lnt containing additional PClint arguments. args.lnt is a text file where every line is an argument for the PClint, example:

```
-e537
-e451
```

## Execute python scripts standalone

```bash
cd "scripts"
python3 -m c_parser_src <path_to_analyse>
```

```bash
cd "scripts"
python3 -m pclp_out_interpret_src <pclp_out_file>
```

```bash
pclp_juliet_a>python scripts\reduced.py ".\test" "ignore_modules.txt"
```

## Execute pylint

```bash
pclp_juliet_a>pylint scripts\reduced.py
pclp_juliet_a>pylint scripts\processor.py
pclp_juliet_a>pylint scripts\ignore_list.py
pclp_juliet_a>pylint scripts\pclp_out_interpret_src
pclp_juliet_a>pylint scripts\c_parser_src
```

# Processing diagrams

```
info=true
warning=true
supplemental=true
generate-output=        
```