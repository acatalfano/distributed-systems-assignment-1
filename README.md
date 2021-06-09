# distributed-systems-assignment-1

Single Broker-Based Pub-Sub Using ZMQ and Mininet

## installation

Clone this repository, then open a terminal in the root directory.
You will first setup a virtual environment and then install all dependencies in developer mode.

Make sure you have at least `Python 3.9` installed. This has been tested with version 3.9.4.
Also ensure that you have the latest `pip` and that it points to a `Python 3.9` installation.

If you want to run the files locally, a `venv` is recommended. If you want to run the mininet scripts,
a `venv` won't be much help since you need to run the python scripts as `sudo`.

### venv -- For running locally

Also ensure that your python installation includes `venv`.
If you have the option at installation, this means selecting the "full" version.

Open up a terminal in the root directory of this repository and run the following command.
For Windows: `py -m venv ./env`
For Linux: `python3 -m venv ./env` the command might be `python3.9` or `python`, depending how it is aliased in your system.

Run the following command.
For Windows: `./env/Scripts/activate`
For Linux: `source ./env/bin/activate`

### mininet setup

You will need to first have a system compatible with running mininet, follow Mininet's [instructions](http://mininet.org/download/) to do so.

You'll need to upgrade python to 3.9 and pip along with it. The install instructions assume a recent Ubuntu environment.

#### Install Python 3.9

Before beginning, update and ensure `software-properties-common` is installed:

```bash
$ sudo apt update
$ sudo apt install software-properties-common
```

Now add the PPA:

```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa
```

Install Python3.9:

```bash
$ sudo apt install python3.9
```

Alternatively, you may want to install `python3.9-full`, which you can always do later if necessary.

You can now run Python 3.9 with the command `python3.9`. For sanity, check the version with `python3.9 --version`.

#### Install Pip for Python 3.9

Retrieve and run the `get-pip.py` script:

```bash
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ sudo python3.9 ./get-pip.py
```

Cleanup the script if you want; it served its purpose.

```bash
$ rm ./get-pip.py
```

### Install the project dependencies -- For venv or mininet setup alike

Run the following command (all systems)
`pip install -e ./src`

## Running Mininet

To run mininet, you'll have to also install the the ovs test controller. On Ubuntu you'd run:

```bash
$ sudo apt install openvswitch-testcontroller
```

You can run the latency test file by navigating to the directory `src/test/latency` and running:

```bash
$ sudo python3.9 ./topology.py
```

If you get an error output asking you to shut down a controller that's running on some specific port,
you will need to just kill that process.

Discover which process you need to kill by running:

```bash
$ ps -aux | grep controller
```

The number in the second column is the process ID you are after. You may get multiple processes, the one you're after
is probably the one running on `root` (not the user process). Kill one process at a time until you don't get the
error message anymore.

```bash
$ sudo kill [PID]
```
