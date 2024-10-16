# Pepline for IEDB Next-Generation Tools T Cell Class I 

**Designed by qinti in 20241012**
### Prerequisites

+ Linux 64-bit environment
  * http://www.ubuntu.com/
    - This distribution has been tested on Linux/Ubuntu 64 bit system.
+ Python 3.8 or higher
  * http://www.python.org/
+ tcsh
  * http://www.tcsh.org/Welcome
    - Under ubuntu: sudo apt-get install tcsh
+ gawk
  * http://www.gnu.org/software/gawk/
    - Under ubuntu: sudo apt-get install gawk

### Downloading from IEDB website

### Installation

```{shell}
tar -xvzf IEDB_NG_TC1-VERSION.tar.gz
mamba create -n IEDB python=3.10
mamba activate IEDB
pip install -r requirements.txt -i https://mirrors.zju.edu.cn/pypi/web/simple
PIP_CONSTRAINTS=pip_constraints.txt pip install -r requirements.txt
pip install numpy==1.24.4
```

### Easy-usage

#### Step1

```{shell}
python fasta_to_json.py input_sequence.fasta output.json
```

#### Step2

```{shell}
python3 src/tcell_mhci.py -j output.json --split --split-dir="./test/"
```

#### Step3

```{shell}
python IEDB_predict.py job_descriptions.json
```



