# SMS-manipulation-detection-tool
The SMS-manipulation-detection-tool determines whether an Android mobile phone text message has been tampered with.


## usage : 

  messageDet.exe [start datetime] [end datetime]
  
* start_datetime : The starting date and time for the analysis  (format: yyyymmddhhmmss)'
* end datetime   : The ending date and time for the analysis (format: yyyymmddhhmmss)'

## Example :

  Here is an example of how to use the tool:
* messageDet.exe 20230601000000 20230630235959

## Cautions
Please be aware of the following cautions before using this tool:

1. Installing ADB (Android Debug Bridge) : ADB is a command-line tool that allows you to communicate with Android devices. 
2. Accurate Date and Time Format: The tool requires dates to be in the exact yyyymmddhhmmss format. Incorrect formatting may result in errors or inaccurate analysis.

[adb 관련 정보](https://developer.android.com/tools/adb)
