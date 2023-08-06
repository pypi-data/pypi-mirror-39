# TRON-CLI
```
 _________  ____  _  __    _______   ____
/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
 / / / , _/ /_/ /    /___/ /__/ /___/ /  
/_/ /_/|_|\____/_/|_/    \___/____/___/
```

A command line tool, to quick set up, turn on/off (multiple) tron nodes(full/solidity), and monitor running status.

| Python | JDK |
|--------|-----|
| 3.7+   | 1.8 |

* Learn more about tron on [TRON Developer Hub](https://developers.tron.network/docs/full-node)

* Join the community on [TRON Discord](https://discord.gg/GsRgsTD)

* Source code on [Github](https://github.com/tronprotocol/tron-cli)

* Project on [Pypi](https://pypi.org/project/troncli/)

## Install

### pip

> pip install --upgrade pip

```
pip install troncli
```

#### FAQs on installation

1. How to fix "fail to build a wheel for psutil" error?

    a. please check if you installed clang correctly, or install it using homebrew:

    ```
    brew install --with-toolchain llvm
    ```

    b. please check if you are using python 3.x

2. How to test in virtual environment?
    
    a. create virtual environment

    ```
    python3 -m venv venv
    ```

    b. activate venv

    ```
    . ./venv/bin/activate
    ```

    c. install troncli in venv

    ```
    pip install troncli
    ```

    d. when done testing, or using the venv - to deactivate venv

    ```
    deactivate
    ```

## Usage

| Command                                                                              | Functions                          | Example1        | Example2                                                                                                      |
|--------------------------------------------------------------------------------------|------------------------------------|-----------------|---------------------------------------------------------------------------------------------------------------|
| tron-cli init --version                                                              | Init dirs and fetch code.          | tron-cli init   | tron-cli init --version 3.1.3                                                                                 |
| tron-cli config --nettype --fullhttpport --solhttpport --fullgrpcport --solgrpcport  | Create and customize config files. | tron-cli config | tron-cli config --nettype main --fullhttpport 8500 --solhttpport 8600 --fullgrpcport 50051 --solgrpcport 5001 |
| tron-cli run --nodetype                                                              | Run node.                          | tron-cli run    | tron-cli run --nodetype sol                                                                                   |
| tron-cli stop --pid                                                                  | Stop node.                         | tron-cli stop   | tron-cli stop --pid 7777                                                                                      |
| tron-cli status --node                                                               | Monitor nodes status.              | tron-cli status | tron-cli status --node 777                                                                                    |
| tron-cli quick                                                                       | Quick start.                       | tron-cli quick  | tron-cli quick                                                                                                |
| tron-cli -h, --help                                                                  | Check help manual.                 | tron-cli -h     | tron-cli --help                                                                                               |
#### overall

```
tron-cli -h
```
```
usage: tron-cli [-h] {init,config,run,stop,status,quick} ...

which subcommand do you want?

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {init,config,run,stop,status,quick}
    init                Init dirs and fetch code.
    config              Create customize config files.
    run                 Run node.
    stop                Stop node.
    status              Monitor nodes status.
    quick               Quick start. (run a full private node by one command)
```

##### subcommand: init

```
tron-cli init -h
```
```
usage: tron-cli init [-h] [--version VERSION]

optional arguments:
  -h, --help         show this help message and exit
  --version VERSION  specify java-tron version
```

##### subcommand: config

```
tron-cli config -h
```
```
usage: tron-cli config [-h] [--nettype NETTYPE] [--fullhttpport FULLHTTPPORT]
                       [--solhttpport SOLHTTPPORT] [--fullrpcport FULLRPCPORT]
                       [--solrpcport SOLRPCPORT] [--enablememdb ENABLEMEMDB]

optional arguments:
  -h, --help            show this help message and exit
  --nettype NETTYPE     specify net type [main, private]
  --fullhttpport FULLHTTPPORT
                        specify full http port
  --solhttpport SOLHTTPPORT
                        specify solidity http port
  --fullrpcport FULLRPCPORT
                        specify full rpc port
  --solrpcport SOLRPCPORT
                        specify solidity rpc port
  --enablememdb ENABLEMEMDB
```

##### subcommand: run

```
tron-cli run -h
```
```
usage: tron-cli run [-h] [--nodetype NODETYPE]

optional arguments:
  -h, --help           show this help message and exit
  --nodetype NODETYPE  specify node type [full, sol]
```

##### subcommand: stop

```
tron-cli stop -h
```
```
usage: tron-cli stop [-h] --pid PID

optional arguments:
  -h, --help  show this help message and exit
  --pid PID   stop node by given pid
```

##### subcommand: status

```
tron-cli status -h
```
```
usage: tron-cli status [-h] [--node NODE]

optional arguments:
  -h, --help   show this help message and exit
  --node NODE  check specific node detail by pid
```
