# Leakdown Tester Script User Manual
### Welcome to the user manual for the Leakdown Tester Script!
Fun Facts:
- The script is named after a testing protocol for testing engine blocks, the reverse of a compression test. Pressurized air is introduced to the engine block to check for leaking points - just like how this script can be used to check if the pipeline holds "water"!
- Environment variables will save you time, especially if you make them persistent!
- Nobody will read this!

## Environmental Variables
1) `CSVPATH` - Filepath to a local CSV file. 
The script checks for this on startup, as some kind of JSON content for the POST request is required. You can specify this filepath with the csv argument, or you can set the env var and specify a different filepath with the csv argument which will override the environment variable. A filepath must be specified if not using the useGit argument.
2) `PFP` - URL of the PFP API endpoint where the POST requests are sent.
It is likely faster to use the `--target` argument to set the API endpoint rather than to set the environment variable here, however both methods are implemented. Use what works for you.
3) `TARGET_AUDIENCE` - This target_audience variable is the target audience of the API,connect with the developer to get the details, as it depends on the security of the API.

## Arguments
Below are the argument that can be used to run the script. Initializing with all default values will yield a single post request sent to a locally hosted PFP instance.

Format:
- `--argument` `valid input` : Details about the argument.

### Integer Args
- `--RI` `X` : Integer, default 0. The first row of data read from the specified CSV file.
- `--RF` `X` : Integer, default 12. The last row of data read from the specified CSV file. Change this in multiples of 12 to include full "years" of data from the CSV file.
- `--C` `X` : Integer, default 10. The number of columns of data to read from the CSV file. Only change when working with deprecated pipeline versions that do not accept MPOG Goal inclusion. 
- `--reqs` `X` : Integer, default 1. Number of post requests sent by the script to the API endpoint.


### String Args
- `--target` `local` : String which the script parses and uses to set the API endpoint for the POST requests. Use "local", "heroku", or "cloud".
-  `--csv` `"filepath to CSV"` : Use double quotation marks around the filepath to your local copy of the MPOG-like test data CSV file. Note: it is better to set the filepath as an environmental variable, but this functionality is fully implemented.
- `--useGit` `"link"` : Paste a link to a GitHub `input_message.JSON` file inside "" to pull that JSON file in and use the script to send copies of it to the chosen endpoint.
-  `--service_account` `"filepath to service account"` : Use double quotation marks around the filepath to your local copy of the service_account. Note: it is better to set the filepath as an environmental variable, but this functionality is fully implemented.Connect with the developer to get the details, as it depends on the security of the API.

### Logical Args ("Store True")
Adding these arguments to your initialization will change the output you recieve on a successful POST request.

- `--respond` : Logical T/F, default False. Adding to your initialization will have the script print a subset of the JSON data returned from a successful POST request to the pipeline.
- `--save` : Logical T/F, default False. Adding to your initialization will have the script save the JSON content AND the pictoralist image of the output message to your machine, and will tell you what it has named the files.

## Setup
1) Download the entire Leakdown Testing folder from the PFP github repository
2) Find the folder in your file browser, we will need some filepaths later
3) That's all!

### Setting up Environment Variables
Env Var declaration is OS dependent, and can be rather annoying, especially for my Windows friends. 
For my windows warriors:
- Use this to set a temporary env var in this command prompt instance only:
```shell
set CSVPATH="[filepath to CSV]"
```
- With admin privs, you can set a persistant env var:
```shell
setx CSVPATH "[filepath to CSV]"
```
Verify the changes took, which might require reloading your command prompt. Check with the following:
```shell
echo $ENV:CSVPATH
```
Verify that it reads back correctly.

---
Mac users, you can do pretty much the same thing with less headache:
```bash
export CSVPATH=/filepath to CSV.csv
```
There is a way to make it persist, though it requires changing the config of your shell, whoch should be somwhere like `/bin/bash`, etc. 
Use 
```bash
echo $SHELL
```
then open an IDE like nano or Vim, whatever you have:
```bash
nano ~/.bash_profile
```
Then add a line like the export statement writen at the top of the Mac section. 
Then reload your console, you can use a console prompt for that:
 ```bash
 source ~/.bash_profile
```
Whatever works for you!
