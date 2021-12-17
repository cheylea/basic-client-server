# Client/Server Network

This project contains both the server and client functionality for sending a dictionary and text file from a client to a server with different serialisation, encryption and input/output options.

## Directory
```
C:.
│   dependencies.txt
│   README.md
│   LICENSE
│   setup.py
│
├───src
│       BestWords.txt
│       client.py
│       server.py
│
└───test
        unittest_client.py
        unittest_server.py
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install -r dependencies.txt
```

## Usage
To use the network, run each script in its own terminal window.

### Server 
Open terminal window, navigate to **src** directory path and run the following:
```
python server.py
```

The output in the window will be the following:
```
Server Open on 127.0.0.1:5000
```

### Client
Open terminal window, navigate to **src** directory path and run the following:
```
python client.py
```
The output in the window will be the following:
```
### Serialization Section ###
### Do you wish to manually enter a dictionary? (Y) (N) ###
```
Follow the indicated steps in the terminal window in order to send an input to the server. Included in the src folder is `BestWords.txt`, an example text file that can be used to experiment with sending to the server. 
If using a file in a different location, input the full path.

### Example Usage
Example of of using the programme below:

![](https://i.imgur.com/nxRq3Uu.gif)


## Tests
### Server 
Open terminal window, navigate to **src** directory path and run the following:server.py script.
```
python server.py -T
```

The output in the window will be the following:
```
Server Open on 127.0.0.1:5000
```

### Client
Open terminal window, navigate to **test** directory path and run the following:
```
python unittests_client.py
```
```
python unittests_server.py
```
The output in the window will reflect the result of the tests. You may need to run the server command again if the server times out.

### Example Usage
Example of test results shown below:

![](https://i.imgur.com/YjNGTc1.gif)


## Contributing
Pull requests permitted. When contributing please update the test directory as appropriate with any additional requirements. 
