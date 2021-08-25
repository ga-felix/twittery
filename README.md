## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Modules](#modules)
* [Setup](#setup)

## General info
This software extracts data from Twitter and populates
a MySQL database. Therefore, the database is used to
create a network to be used later.

## Technologies
Project is created with:
* Python: 3.6
* MySQL Workbench: 8.0
* Networkx: 2.5.1
* pymysql: 1.0.2

Python, MySQL and mentioned python modules are
all requirements to run this software. 

## Modules
The software consist of these following modules,
all of them storaged on 'src' folder:
* extractor: extracts data from Twitter.
* database: populates SQL database.
* api: performs Twitter API calls.
* reporter: generates the graph.
'settings' and 'interface' modules are still
being created.

## Setup
To run this project, install it using 'install'
file, available on root directory:

```
$ cd ../twittery
$ sudo pip3 install -r requirements.txt