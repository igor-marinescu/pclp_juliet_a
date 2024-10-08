
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
pip3 install matplotlib
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
sudo apt install python3-matplotlib
```

### Build imposter with gcc

```bash
cd ~/pclint/pclp/config
gcc imposter.c -o imposter
```

## Prepare pclp_juliet_a

### Clone pclp_juliet_a repository

```bash
mkdir ~/Work
cd ~/Work
git clone "https://github.com/igor-marinescu/pclp_juliet_a.git"
```

Set execution permissions for ig1.sh script:

```bash
chmod u=rwx,g=r,o=r ~/Work/pclp_juliet_a/ig1.sh
```

### Copy Juliet Test Suite

Download Juliet Test Suite from https://samate.nist.gov/SARD/test-suites/112

Copy the downloaded test suite:

```bash
mkdir ~/Work/juliet_test_suite
cp 2017-10-01-juliet-test-suite-for-c-cplusplus-v1-3.zip ~/Work/juliet_test_suite/
```

Unzip it:

```bash
cd ~/Work/juliet_test_suite/
unzip 2017-10-01-juliet-test-suite-for-c-cplusplus-v1-3.zip
```

## Excute ig1.sh bash-script

```bash
cd ~/Work/pclp_juliet_a/
 ./ig1.sh ~/Work/juliet_test_suite/C/
```

The script loads the file args.lnt containing additional PClint arguments. 
args.lnt is a text file where every line is an argument for the PClint, example:

```
-e537
-e451
```

The scripts searches all Makefiles inside of the directory passed as argument and invokes PC-lint for every makefile found:

```bash
$ ./ig1.sh ~/Work/juliet_test_suite/C/
[INFO] PCLint extra options: /home/igor/Work/pclp_juliet_a/args.lnt
[INFO] WORKING_DIR=/home/igor/Work/juliet_test_suite/C
[INFO] GCC_EXE=/usr/bin/gcc
[INFO] PCLP_PATH=/home/igor/pclint/pclp
[INFO] Generate compiler configuration
[  1/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE400_Resource_Exhaustion/s02/Makefile
[  2/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE400_Resource_Exhaustion/s01/Makefile
[  3/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle/Makefile
[  4/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE190_Integer_Overflow/s03/Makefile
[  5/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE190_Integer_Overflow/s02/Makefile
...
```

For every makefile found, a similar directory is created in `<directory to analyze>/ig_gl_out` folder.
The PC-lint generated results are stored in ig_pclint_out.txt file:

```bash
$ find ~/Work/juliet_test_suite/C/ -name "ig_pclint_out.txt"
/home/igor/Work/juliet_test_suite/C/ig_gl_out/testcases/CWE400_Resource_Exhaustion/s02/ig_pclint_out.txt
/home/igor/Work/juliet_test_suite/C/ig_gl_out/testcases/CWE400_Resource_Exhaustion/s01/ig_pclint_out.txt
/home/igor/Work/juliet_test_suite/C/ig_gl_out/testcases/CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle/ig_pclint_out.txt
/home/igor/Work/juliet_test_suite/C/ig_gl_out/testcases/CWE190_Integer_Overflow/s03/ig_pclint_out.txt
/home/igor/Work/juliet_test_suite/C/ig_gl_out/testcases/CWE190_Integer_Overflow/s02/ig_pclint_out.txt
```

### TODO:

There is a Makefile in Juliet root folder (./C/Makefile). 
This file is processed at the end. 
It should not be processed. It fails:

```bash
igor@ubuntig:~/Work/pclp_juliet_a$ ./ig1.sh ~/Work/juliet_test_suite/C/
[INFO] PCLint extra options: /home/igor/Work/pclp_juliet_a/args.lnt
[INFO] WORKING_DIR=/home/igor/Work/juliet_test_suite/C
[INFO] GCC_EXE=/usr/bin/gcc
[INFO] PCLP_PATH=/home/igor/pclint/pclp
[INFO] Generate compiler configuration
[  1/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE400_Resource_Exhaustion/s02/Makefile
[  2/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE400_Resource_Exhaustion/s01/Makefile
[  3/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle/Makefile
...
[152/153] /home/igor/Work/juliet_test_suite/C/testcases/CWE510_Trapdoor/Makefile
[153/153] /home/igor/Work/juliet_test_suite/C/Makefile
ld: cannot find CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_01.o: No such file or directory
ld: cannot find CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_02.o: No such file or directory
ld: cannot find CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_03.o: No such file or directory
ld: cannot find CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_04.o: No such file or directory
...
ld: cannot find CWE121_Stack_Based_Buffer_Overflow__CWE193_char_alloca_cpy_82_bad.o: No such file or directory
ld: cannot find CWE121_Stack_Based_Buffer_Overflow__CWE193_char_alloca_cpy_82_goodG2B.o: No such file or directory
make[1]: *** [Makefile:49: partial.o] Error 1
make: *** [Makefile:24: testcases/CWE121_Stack_Based_Buffer_Overflow/s01/partial] Error 2
[ERROR] pclp64_linux finished with error:
/home/igor/Work/juliet_test_suite/C/ig_gl_out/./ig_project.lnt, 4, warning, 686
/home/igor/Work/juliet_test_suite/C/ig_gl_out/./ig_project.lnt, 5, error, 305
```

## Prepare reduced python-script

Install python venv:

```bash
sudo apt install python3-venv
```

## Excute reduced python-script

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 scripts/reduced.py ~/Work/juliet_test_suite/C/ ignore_modules.txt

```

### TODO:

Error in python:
```bash
Traceback (most recent call last):
  File "/home/igor/Work/pclp_juliet_a/scripts/reduced.py", line 259, in <module>
    generate_plot_data(pclp_msg, pr)
  File "/home/igor/Work/pclp_juliet_a/scripts/reduced.py", line 167, in generate_plot_data
    generate_pie.gen_plt(pies_data)
  File "/home/igor/Work/pclp_juliet_a/scripts/generate_pie.py", line 146, in gen_plt
    gen_pie(axes[i][j], pie_data[i][j])
  File "/home/igor/Work/pclp_juliet_a/scripts/generate_pie.py", line 84, in gen_pie
    slices_colors.append(pie_data[2]["others"])
                         ~~~~~~~~~~~^^^^^^^^^^
KeyError: 'others'
(.venv) igor@ubuntig:~/Work/pclp_juliet_a$
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
