# TCP Server for tk102-2 GPS
Simple TCP server written in python3 for the GPS Tracker tk102-2

## Installation
You must have a MySQL compatible DB server configured an running with a database created, with the following tables

```sql
CREATE TABLE `device` (
  `id` char(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `location` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `device_id` char(12) NOT NULL,
  `lat` float(9,6) NOT NULL,
  `lng` float(9,6) NOT NULL,
  `speed` float DEFAULT NULL,
  `date` datetime NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `availability` char(1) NOT NULL,
  `iostate` varchar(100) DEFAULT NULL,
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `location_device_FK` (`device_id`),
  CONSTRAINT `location_device_FK` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=379 DEFAULT CHARSET=utf8;
```

Install PyMySQL driver on your python path

## Configuration
The configuration is stored in a single file named config.txt with the following content:

```
[server]
host = your_host
port = your_port

[database]
host = mysql_host
user = mysql_user
password = mysql_pass
db = gps
```

## Usage
Configure your GPS tk102-2 unit to use GPRS instead of SMS, send the following commands via SMS (asuming the default password is 123456):
* apn123456 your.provider.apn
* adminip123456 your_host your_port
* gprs123456

Configure your GPS tk102-2 unit to send its ubication every X minutes indefinitly, send an SMS:
* t010m***n123456 (every 10 minutes in this example)

In case you want to stop your device sending ubication updates, send an SMS:
* notn123456

Run the server
```
python gps.py
```
