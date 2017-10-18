# Log redactor
Replaces lines of text in a log file if they have a key.  Assumes that entries have a key/value delimiter that is easy to split on.
Assumes text has a format of where the keys are at the end of each line:

XXX XXX FIELD: KEY="VALUE", KEY="VALUE", ... 

## Usage
usage: redact_logs.py [-h] -f FILES [FILES ...] -k KEYS [KEYS ...] [-l LOG]
                      [--field FIELD] [-d DELIMITER]

Redact lines from input gzip file containing fields passed as parameter

<pre>optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        <Required> list of files delimited with spaces
  -k KEYS [KEYS ...], --keys KEYS [KEYS ...]
                        <Required> list of fields that will cause a line to be
                        redacted
  -l LOG, --log LOG     <Optional> location of log file. default is
                        redacted.log
  --field FIELD         <Optional>String that begins fields to examine
  -d DELIMITER, --delimiter DELIMITER
                        <Optional> Field delimiter inside of fields to examine
</pre>
