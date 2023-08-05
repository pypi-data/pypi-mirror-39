**The most useful package for you, young s7_it programer :)**

# How to use it

## logging

```
# Import necessary functions
from divinegift.logger import log_info, log_err, log_warning, set_loglevel

# info msg
log_info('Your message')

# error msg 
log_err('Error msg',
	    src='Error source',  # e.g. str(sys.argv[0])
	    mode=['telegram', 'email']  # May be empty
	    channel={ "telegram": -1001343660695, "email_to": ["youremail@s7.ru"]})  # You can add "email_cc" for add copy_to address

# error msg with out sending problem to external system
log_err('Error msg', src='Error src') 
```

## Pass log_level and log_name through cmd arguments

To specify log_level and log_name to your app you can send it through arguments:
```
if __name__ == '__main__':
	# Get all args from cmd:
    args = get_args()
    # Get log_level, log_name, log_dir
    lp = get_log_param(args)
    # Set log_level and log_name:
    set_loglevel(lp.get('log_level'), lp.get('log_name'), lp.get('log_dir'))
```
You should pass your args by pairs: key value, e.g. --log_level INFO
Available variants for logging are:
* --log_level or shortcut is -ll
* --log_name or shortcut is -ln
* --log_dir or shortcut is -ld

log_level could be DEBUG, INFO, WARNING, ERROR

Example of start apps with arguments:
```
python test.py -ll INFO -ln test.log
```

## Config parsing (json)

```
from divinegift.smain import Settings  # Necessary imports
 
settings = {} 

# You should use divinegift.logger.set_loglevel before config parsing
s = Settings()
s.parse_settings('./settings.conf')
settings = s.get_settings()
```

## Config example

```
{
    "log_level": "INFO",
    "log_name": "YourAwesomeProject.log",
    "monitoring": [
        "telegram",
        "email"
    ],
    "monitoring_channel": {
        "telegram": -1001343660695,
        "email_to": [
            "aims.control@s7.ru"
        ]
    }
 }
```

## Working with DB (sqlalchemy)

You should define dict with db_conn creditional.
For example:

### Oracle
Install oracle driver:
```
pip install cx_oracle
```
```
db_conn = {
	"db_user": "dbuser",		# username
	"db_pass": "dbpass",		# password
	"db_host": "dbhost",		# host (ip, fqdn). could be empty if we connect via tns
	"db_port": "",				# port (string). could be empty if we connect via tns 
	"db_name": "dbname",		# database name
	"db_schm": "",				# db scheme if not equal username
	"dialect": "oracle"	# 		# if use cx_Oracle or oracle+another_dialect
}
```
### MSSQL
Install mssql driver:
```
pip install sqlalchemy-pytds
```
```
db_conn = {
	"db_user": "dbuser",		# username
	"db_pass": "dbpass",		# password
	"db_host": "",				# host (ip, fqdn). could be empty if we connect via tns
	"db_port": "",				# port (string). could be empty if we connect via tns 
	"db_name": "dbname",		# database name
	"db_schm": "",				# db scheme if not equal username
	"dialect": "mssql+pytds"	# mssql dialect
}
```
### Postgres
Install postgres driver:
```
pip install psycopg2
```
```
db_conn = {
    "db_user": "dbuser",		# username
	"db_pass": "dbpass",		# password
	"db_host": "",				# host (ip, fqdn). could be empty if we connect via tns
	"db_port": "",				# port (string). could be empty if we connect via tns 
	"db_name": "dbname",		# database name
	"db_schm": "",				# db scheme if not equal username
    "dialect": "postgresql+psycopg2" # dialect
}
```

### Create connect

For create connect you should use function *divinegift.smain.get_conn*.
```
from divinegift.smain import get_conn, close_conn
engine, conn, metadata = get_conn(db_conn)  # db_conn - variable which was described above
```

If you need to call stored procedure with db cursors you should use raw connection.
```
from divinegift.smain import get_raw_conn
conn = get_raw_conn(db_conn)  # db_conn - variable which was described above
```

### Get data from sript (file or just string)

When you got "conn" variable you can  get data from file or from str variable directly.

```
result = get_data('path/to/scripts/some_script.sql', db_conn)
# or you can use str variable:
script = 'select * from dual'
result = get_data(script, db_conn)
print(result)
>>>[{'dummy': 'X'}]
```

You can use specific encoding for your files (by default it's 'cp1251'). 
Just put it into args:
```
result = get_data('path/to/scripts/some_script.sql', db_conn, encoding='utf8')
```

Also you can add some variables into your script (e.g. date) and then you can pass it into function:
```
script = """select * from dual
where dummy = '$param'"""
parameters = {'param': 'X'}
result = get_data(script, db_conn, **parameters)
# Or another variant
result = get_data(script, db_conn, param='X')
print(result)
>>>[{'dummy': 'X'}]
```

### Run script without getting data

You can run script without recieving data.
You should use *divinegift.smain.run_script* for this like get_data, e.g.:
```
run_script('path/to/scripts/some_script.sql', db_conn)
```

## Sending email

You can use function *divinegift.smain.send_email*

You should set your msg, subject and list of recipients.
Simple example:
```
from divinegift.smain import send_email
send_email('Test message', 'Test subject', TO=['your@domain.com'])
```

You can specify TO, CC, BCC, HOST, FROM and attachments. Also you can send it like html-message or like text.

You should pass list of attachments files with absolute path to it. You can use function *divinegift.smain.get_list_files* for get it.
For sending email with attahment(s):
```
from divinegift.smain import send_email, get_list_files
attachment_list = get_list_files('/path/to/files', add_path=True)
send_email('Hello! This are files in attach', 'Test sending attachments', ['your@domain.com'], attachments=attachment_list)
# Also you can send only one file:
attachment = '/path/to/file/file_name'
send_email('Hello! There is file in attach', 'File', ['your@domain.com'], attachments=attachment)
```

If you set IS_HTML to False (by default it is True), you could send an email like simple text message, not html

## Work with JSON

You can simple parse and create JSONs

To create json you should use *divinegift.smain.create_json*
To parse it you shoul use *divinegift.smain.parse_json*

For example:
```
from divinegift.smain import create_json, parse_json
A = {'key1': 'data1', 'key2': 'data2'}
create_json('json_file_name.json', A)
B = parse_json('json_file_name.json')

print(B)
>>> {'key1': 'data1', 'key2': 'data2'}
```
