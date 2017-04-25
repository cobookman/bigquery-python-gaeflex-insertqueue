Simple stupid background streaming insert queuing service.

In production you might want to remove the `time.sleep(1)` in the 
`background_bq.py` script (line 91).

You will also want to remove a lot of the print statements as well.

For this to work the project you are authenticated under needs to have a

* dataset of name `my_dataset`
* table of name my_table with a single column of type `string` with the name
  `some_string_key`


TO queue up a bunch of inserted rows simply call `./example_http_call.sh`
