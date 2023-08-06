## Overview

`short-cli` is a command line utility that can be used to shorten long URLs with 5 different services and then track the total views each one gets. `short-cli` is built with Python and utilizes the APIs for each of these services. 

## Services
`short-cli` works with:
* bit.ly
* tinyurl.com
* is.gd
* v.gd
* tiny.cc

## Installation
`short-cli` can be installed with `pip` or by downloading and compiling the source code. 

## Usage
`short-cli` is very simple to use. Use the command `short` and pass the URL as an argument to get the shortened link as the output. `short-cli` uses bit.ly by default, to use another one of the services just add one of the respective arguments:
* `-t` for tinyurl.com
* `-v` for v.gd
* `-i` for is.gd
* `-c` for tiny.cc

##### Example
`short -t github.com` would shorten github.com with tinyurl.

### Getting Statistics
To get the number of views for the URL simply add the `-w` argument as well as the argument for the service and pass the ID instead of the URL. The ID is the part after the root link, for instance the ID in the short link `http://v.gd/test` is `test`. 

##### Example
`short -v -w test` would get the number of views for the short link registered with v.gd that has the ID `test`. 

