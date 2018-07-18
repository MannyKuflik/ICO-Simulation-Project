CREATE DATABASE BROVIS;
use BROVIS;

CREATE TABLE bitcoin (
    id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    address varchar(2048),
    amount varchar(2048),
    txhash varchar(2048),
    xpub NOT NULL varchar(2048),
);

CREATE TABLE ethereum (
    id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    address varchar(2048),
    amount varchar(2048),
    txhash varchar(2048),
    xpub NOT NULL varchar(2048),
);