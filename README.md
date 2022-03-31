Census PL-94 to SQLite3
======

Simple tool to build out the Census PL-94 datasets from the FTP and build a SQLite3 database 

## Usage

```python
getPL94(database, Exists='drop', Table='PL94', Vintage=2020, State=None, Directory=None)
```

### Parameters

database - Name of database you would like to add data to

Exists - **DEFAULT: drop** any SQLite3 command for if_exists prameters

Table - **DEFAULT: PL94** name of table in SQLite database

Vintage - **DEFAULT: 2020** either 2020 or 2010 PL94 dataset are avaible through the FTP

State - **DEFAULT: None** unless secified by full name or 2 letter abberviation will build PL-94 National Dataset

Directory - **DEFAULT: None** dirctory where you would like to write too if not the current directory 

Census Tigerfiles to SQLite3
======

## Usage

```pytnon
getTiger(database, Layer, Table_Name=None, Exists='append', Vintage=2020, State=None, Directory=None, file_to_table=False)
```
### Parameters

database - Name of database you would like to add data to

Exists - **DEFAULT: append** any SQLite3 command for if_exists prameters

Table_Name - Name of table in SQLite database

file_to_table - When True Table_Names will be created using the Tiger File Name 

Vintage - **DEFAULT: 2020** either 2020 or 2010 PL94 dataset are avaible through the FTP

State - **DEFAULT: None** unless secified by full name or 2 letter abberviation will use all avalible files for that layer

Directory - **DEFAULT: None** dirctory where you would like to write too if not the current directory 