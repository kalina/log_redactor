# Log redactor
Replaces lines of text in a gzipped log file if they have a key.  Assumes that entries have a key/value delimiter that is easy to split on.
Creates a new file: redacted_<filename> in gzipped format
Assumes text has a format of where the keys are at the end of each line:

XXX XXX FIELD: KEY="VALUE", KEY="VALUE", ... 

## Usage
<pre>usage: redact_logs.py [-h] -f FILES [FILES ...] -k KEYS [KEYS ...] [-l LOG]
                      [--field FIELD] [-d DELIMITER]

Redact lines from input gzip file containing fields passed as parameter

optional arguments:
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

## Performance considerations
This program can be CPU intensive as it is decompressing and compressing text.  Limiting it's priority (nice) can help limit it's utilization.
The memory footprint remains small as not much is persisted in memory.  The disk utilization is roughly 2x the initial gzip file.
