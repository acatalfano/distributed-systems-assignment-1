# distributed-systems-assignment-1

Single Broker-Based Pub-Sub Using ZMQ and Mininet

## installation

Clone this repository, then open a terminal in the root directory.
You will first setup a virtual environment and then install all dependencies in developer mode.

Make sure you have a recent version of `Python 3`. This has been tested with version 3.9.4.
Also ensure that you have the latest `pip`. Also ensure that your python installation includes `venv`.
If you have the option at installation, this means selecting the "full" version.

### Setup the virtual environment

Open up a terminal in the root directory of this repository and run the following command.
For Windows: `py -m venv ./env`
For Linux: `python3 -m venv ./env` the command might be `python3.9` or `python`, depending how it is aliased in your system.

### Activate the virtual environment

Run the following command.
For Windows: `./env/Scripts/activate`
For Linux: `source ./env/bin/activate`

### Install the project dependencies

Run the following command (all systems)
`pip install -e ./src`
