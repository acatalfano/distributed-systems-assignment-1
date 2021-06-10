# distributed-systems-assignment-1

Single Broker-Based Pub-Sub Using ZMQ and Mininet

## installation

Clone this repository, then open a terminal in the root directory.
You will first setup a virtual environment and then install all dependencies in developer mode.

Make sure you have at least `Python 3.9` installed. This has been tested with version 3.9.4.
Also ensure that you have the latest `pip` and that it points to a `Python 3.9` installation.

If you want to run the files locally, a `venv` is recommended. If you want to run the mininet scripts,
a `venv` won't be much help since you need to run the python scripts as `sudo`.

### mininet setup

You will need to first have a system compatible with running mininet, follow Mininet's [instructions](http://mininet.org/download/) to do so.

Either setup the VM image outlined in option 1 or follow these steps taken from options 2:

Clone the mininet repository and checkout the 2.3.0 branch. There are other more
recent releases of mininet (e.g. `2.3.0d6`), but they had some quirks with packages
not lining up. `2.3.0` is the happy path. You need to install like this because the
latency tests depend on controllers as well as the actual mininet library.
```bash
$ git clone git://github.com/mininet/mininet
$ cd mininet
$ git checkout -b mininet-2.3.0 2.3.0
$ cd ..
```

Now run the installation script:
```bash
$ mininet/util/install.sh -nfv
```

You'll need to upgrade python to 3.9 and pip along with it. The installation instructions
assume a recent Ubuntu environment.

### Install Python 3.9

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

### Install Pip for Python 3.9

Retrieve and run the `get-pip.py` script:

```bash
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ sudo python3.9 ./get-pip.py
```

Cleanup the script if you want; it served its purpose.

```bash
$ rm ./get-pip.py
```

### Setup a Virtual Environment

Your python installation probably includes `venv`, but if not you'll have to get a Python 3.9 distribution that does.
If you have the option at installation, this means selecting the "full" version.

Open up a terminal in the root directory of this repository and run the following command.

```bash
$ python3.9 -m venv --upgrade-deps ./env
```

Activate the venv

```bash
$ source ./env/bin/activate
```

If you close the terminal, you'll have to activate the venv again.

### Install the project dependencies

This will install all of the dependencies except for mininet,
that will be built from source.
Run the following command (all systems)

```bash
$ pip install -e ./src
```

You will now have to copy over the mininet package that was setup for you.
Locate it, likely in `~/.local/lib/python3.9/site-packages`. The `mininet` directory is what you want to copy.
Copy it over to `/PATH/TO/REPOSITORY/env/lib/python3.9/site-packages`

## Running Mininet

You can run the latency test file by navigating to the directory `src/test/latency` and running:

```bash
$ sudo ../../../env/bin/python3.9 ./topology.py [OPTIONS]
```

you may consider making an alias for the venv's python3.9 is you're going to run this a lot

See below for an overview of the CLI options.

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

### topology.py Options

`topology.py` has some rich CLI options to make it fast and easy to run a variety of test setups.

The format is:

```bash
$ sudo PATH/TO/REPO/env/bin/python3.9 ./topology.py OPTIONS SUB-COMMANDS
```

#### OPTIONS

There are 3 options:

* `-s, --sub-count` takes an integer argument, the number of subscriber nodes to spawn in the network
* `-p, --pub-count` same as `--sub-count`, but for publisher nodes
* `-N, --total-topics` takes an integer argument, the number of topics when using the count-based syntax

`-s` and `-p` are both required. `-N` is required if you're using the count-based syntax described in the sub-commands

#### SUB-COMMANDS

There are 2 sub-commands used for specifying behavior on the sub/pub nodes. These commands can be repeated as necessary,
a `pub` sub-command is for describing a single publisher's behavior and a `sub` sub-command is likewise for a subscriber.
Both commands have a count-based and an explicit syntax. The explicit syntax is for specifying explicitly what topics
to publish and subscribe to. The count-based is for specifying larger volumes and you instead specify how many messages/topics,
out of a total of `-N` (from the initial options), the topics themselves are generated under the hood.

##### PUB Sub-Command

```bash
$ pub ID_OPTION (COUNT-BASED-OPTIONS | EXPLICIT-OPTIONS)
```

* `-i, --id` is the ID_OPTION and it takes an integer, a value in the range `[0, P)` where `P` is the max number of publishers
specified in the initial options
* COUNT-BASED-OPTIONS (all are required):
  * `-m, --messages` takes an integer, the number of messages this publisher will publish
  * `-n, --num-t` takes an int, the number of distinct topics to publish
  * `-l, --loop` takes a bool, indicating whether or not to loop infinitely after `m`-many messages are published
  * `-v, --interval` takes a float, the gap of time between published messages
* EXPLICIT-OPTIONS
  * `-t, --topic-freq` takes 2 arguments, a string and an integer, specifying the topic-value and the publishing frequency (in seconds)
  this is the only explicit option, but it is repeated for every topic you would like to publish on this publisher

#### SUB Sub-Command

```bash
$ sub COMMON_OPTIONS (COUNT-BASED-OPTIONS | EXPLICIT-OPTIONS)
```

* COMMON_OPTIONS (all are required):
  * `-i, --id` is the ID_OPTION, it's the same as for `pub`, except it's in the range `[0, S)` where `S` is the max number of subscribers
  specified in the initial options
  * `-w, --wait-time` takes a float, the time in seconds to spin the subscriber's callback
  (called each time a subscribed message is published)
* COUNT-BASED-OPTIONS (all are required):
  * `-n, --num-t` takes an integer, the number of distinct topics to which to subscribe
  * `-v, --interval` takes a float, the time in seconds between each new subscription
* EXPLICIT-OPTIONS
  * `-t, --topic-delay` is much like `-t` in the `pub` options. It can be specified multiple times, once per each
  topic to which the subscriber subscribes. It also takes 2 arguments, a string and an int,
  indicating the topic-value and the time to wait after the previous topic subscription.

## Future Plans

The original intent was to also include a CLI option to pick between different topologies, but the alternate topologies haven't been
developed yet.
`topology.py` has some quirks currently, so it doesn't quite run yet. A couple of development hours are needed to finish that.
Some inevitable bugfixes will be necessary once `topology.py` _does_ work since the other files were only ever run locally
(and the direct_publisher needs to be updated to find its own IP address and send it to the direct_broker instead of sending "localhost",
as it currently does).
Finally, some e2e testing is needed (as well as rounding out `topology.py` to actually get latency results, as opposed to just starting up
a network), then those results will need to be condensed into useful graphics.
