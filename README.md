# mynode
Home Bitcoin Node

Make sure you are in the mynode directory and virtual env.

```
workon mynode
```

Set the python path to the current directory

```
export PYTHONPATH=$PWD
```

### Start bitcoind

We need to make sure we have a local bitcoind server running so open a new terminal and start it like so.

bitcoind -conf=/Volumes/BitcoinSSD/node1/bitcoin.conf -datadir=/Volumes/BitcoinSSD/node1/

Then set the following environment variables such that they match you bitcoin.conf settings

export BC_HOST=localhost
export BC_USERNAME=gnulnx
export BC_PASSWORD=bc
export BC_PORT=8334

### Install pip packages

pip install -r requirements.txt

### Start your node

mynode
mynode --help