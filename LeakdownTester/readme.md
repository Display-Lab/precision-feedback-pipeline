
# Leakdown Tester Script User Manual
### Welcome to the user manual for the Leakdown Tester Script!
Fun Facts:
- The script is named after a protocol for testing engine blocks, the reverse of a compression test. Pressurized air is introduced to the engine block to check for leaking points - it's a metaphor!
- Environment variables will save you time, especially if you make them persistent!
- On average, hedgehogs travel 2.5 miles a day, and average around 40,000 steps to do so! If you were to walk that much, you would travel over 16.5 miles a day!

## Environmental Variables
1) `CSVPATH` - Filepath to a local CSV file. 
The script checks for this on startup, as some kind of JSON content for the POST request is required. You can specify this filepath with the csv argument, or you can set the env var and specify a different filepath with the csv argument which will override the environment variable. A filepath must be specified if not using the useGit argument.
2) `PFP` - URL of the PFP API endpoint where the POST requests are sent.
It is likely faster to use the `--target` argument to set the API endpoint rather than to set the environment variable here, however both methods are implemented. Use what works for you.
3) `TARGET_AUDIENCE` - Variable which contains the "target audience" part of the authentication process for connecting with the GCP PFP API. 
4) `SAPATH` - Variable that sets path to your own Service Account JSON file for use in authorizing POSTs to the GCP PFP instance.

## Arguments
Below are the arguments that can be used to run the script. Initializing with all default values will yield a single post request from CSV file sent to a locally hosted PFP instance.

Format:
- `--argument` `valid input` : Details about the argument.

### Integer Args
- `--tests` `X` : Integer, default 1. Number of Leakdown tests run by the script. To send multiple post requests from CSV or Github sources, increment this accordingly.
- `--threads` `X` : Integer, default 1. Number of threads to run concurrent Leakdown Tests on against the same PFP API endpoint.
- `--RI` `X` : Integer, default 0. The first row of data read from the specified CSV file.
- `--RF` `X` : Integer, default 12. The last row of data read from the specified CSV file. Change this in multiples of 12 to include full "years" of data from the CSV file.
- `--C` `X` : Integer, default 10. The number of columns of data to read from the CSV file. Only change when working with deprecated pipeline versions that do not accept MPOG Goal inclusion. 


### String Args
- `--target` `local` : String which the script parses and uses to set the API endpoint for the POST requests. Use "local", "heroku", or "cloud".
- `--useGit` `"link"` : Paste a link to a GitHub `input_message.JSON` file inside "" to pull that JSON file in and use the script to send copies of it to the chosen endpoint.
- `--persona` `alice` : String representing a persona name from the Knowledge-base's [personas folder](https://github.com/Display-Lab/knowledge-base/tree/main/vignettes/personas). Using this argument will send a single persona's input_message file directly from GitHub as a POST request. Use any of the persona names, in lowercase.
- `--pathway` `social_loss` : String representing a causal pathway from the Knowledge-base's [causal pathway testing suite](https://github.com/Display-Lab/knowledge-base/blob/main/vignettes/dev_templates/causal_pathway_test_suite). Using this argument will send a single causal-pathway input_message file directly from GitHub as a POST request. Use any of the ten implemented causal pathways, in lowercase, with underscores where needed.

-  `--csv` `"filepath to CSV"` : Use double quotation marks around the filepath to your local copy of the MPOG-like test data CSV file. Note: it is better to set the filepath as an environmental variable, but this functionality is fully implemented.
-  `--service_account` `"filepath to service account"` : Use double quotation marks around the filepath to your local copy of the service account file. Note: it is better to set the filepath as an environmental variable, but this functionality is fully implemented. Access to the service account file details are controlled, connect with the developers to get access.

### Logical Args ("Store True")
Adding these arguments to your initialization will change the output you recieve on a successful POST request.

- `--respond` : Adding to your initialization will set to `True`, and have the script print a subset of the JSON data returned from a successful POST request to the pipeline.
- `--save` : Adding to your initialization will set to `True`, and have the script save the JSON content AND the pictoralist image of the output message to your machine, and will tell you what it has named the files.
- `--allPersonas` : Adding to init will set to `True`, and test all 7  persona-based input_message.json files in the Knowledge-base's [personas folder](https://github.com/Display-Lab/knowledge-base/tree/main/vignettes/personas) against a chosen API endpoint.
- `--allCPs`: Adding as an arg will test the ten causal pathway-based JSON files in the Knowledge-base's [causal pathway testing suite](https://github.com/Display-Lab/knowledge-base/blob/main/vignettes/dev_templates/causal_pathway_test_suite) against the selected API endpoint.
- `--vignVal` : Adding to init will set to `True`, and compare the `staff_number`, `acceptable_by`, and `measure` key values in the output message against a set of known valid pairings that are described by the vignettes for each persona.
- `--cpVal` : Adding to init alongside either --pathway or --allCPs will compare the causal pathway selected by the API in the response message against the user-specified causal pathway. Only for use with the causal pathway testing suite.

## Setup
1) Download the entire Leakdown Testing folder from the PFP github repository
2) Find the folder in your file browser, we will need some filepaths later
3) That's all!

### Setting up Environment Variables
Env Var declaration is OS dependent, and can be rather annoying, especially for my Windows friends. 
For my windows warriors:
- Use this to set a temporary env var in this command prompt instance only:
```shell
set VARNAME="content"
```
- With admin privs, you can set a **persistant** env var:
```shell
setx VARNAME "content"
```
Verify the changes took, which might require reloading your command prompt. Check with the following:
```shell
echo $ENV:VARNAME
```
Verify that it reads back correctly.

---
Mac users, you can do pretty much the same thing with less headache:
```bash
export VARNAME=/content/you/want
```
There is a way to make it persist, though it requires changing the config of your shell, which should be somwhere like `/bin/bash`, etc. 
Use:
```bash
echo $SHELL
```
Then open an IDE like nano/Vim/Sublime/whatever, and use the following:
```bash
nano ~/.bash_profile
export export VARNAME=/content/you/want
```
Then reload your console, you can use a console prompt for that:
 ```bash
 source ~/.bash_profile
```
Whatever works for you!
## Setting up Google Cloud Authentication
1) Contact the developers to get access to the client secret details (service account and target audience)
2) Create your service account file
   - Make sure to save it as a .json file, with the proper encoding
   - Copy the file as a path with right click, or any way you like.
3) Set your SAPATH environmental variable
   - Use the guidance in the above section on setting env vars if you get confused
   - Set SAPATH to "path\to\service_acccount_details.json"
4) Set your TARGET_AUDIENCE environmental variable
   - Using the target audience string you recieved by asking for it from someone who knows it, set the env var TARGET_AUDIENCE to "target audience string details"