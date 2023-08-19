# Changelog for Leakdown Tester Script
## Version 1.5.0
Released 8/19/23
- Added multithreading capability to the script
	+ use `--threads X` to start multiple threads to run requests simultaneously against the pipeline.
	+ Changed request naming convention, allow save_resp to work properly
	+ Many structural changes to support multithreading

- Renamed `send_req` and `send_iap_req` to `..._post`
	+ Renamed to more precisely describe their functions
- Added function `post_and_respond`
	+ Refactored the logic for determining which kind of post request to send based on target to this function
	+ Included call to handle_response here so that responses can still be logged, printed, or validated against vignette values

## Version 1.4.3
Resleased 8/18/23
- Updated handle_response() function
	+ Refactored code to check first for 200 status code response, THEN to pull JSON keys for vignette validation
	+ Allows for increased description of bad API responses
	+ Refactoring into handle_response eliminates 8 lines of code from script
- Updated test_persona() function
	+ Allow function to send requests to GCP API
	+ Altered print statement to remove unnecesary request # reporting
	+ Removed total request argument as now unnecessary
- Changed arg `--reqs` to `--tests`
	+ Reflects that some test modes can send upward of one request
	+ Changed codebase to reflect naming convention change
	+ Changed readback statements to show which test loop is running
- Renamed/reworked function `confirm_content`, now `set_behavior`
	+ Function now determines what kind of test for the script to run with logicals, as well as handle the errors of the old function
- Removed function `startup_checklist`
	+ Going forward, startup functions will now print a readback statement to the user as they set configuration details for the script
	+ This cuts down on the amount of logical processes done by the script, but does decrease readability somewhat
- Added function `calc_total_reqs`
	+ Function calculates the total number of POST requests the script will send for each initialization of the script
	+ Will become more important as multithreading is implemented
- Renamed `validate_output` to `response_vign_validate`
	+ Changed to better reflect what the function is accomplishing (increased clarity)
- Updated `main`
	+ With inclusion of "set_behavior", can now much more clearly follow how Post requests are being sent differently based on the test behavior desired
	+ Included all function calls that send a POST in the "Send POST requests" loop

## Version 1.4.2
Released 8/16/23
- Added env var "SAPATH"
	+ Allows path to Service Account file for GCP testing to be set with env var
- Added argument "persona"
	+ Used to test single persona data from knowledgebase input_message files
		* Will be helpful for debugging individual errors down the line (eg Fahad, Gaile bugs currently being encountered)
- Reworked argument and env var declaration and conflict handling
	+ in-line assignment of args and env vars - decreases number of vars used overall
	+ Removed if statements from `confirm_target` to support above
- Worked on GCP testing functionality
	+ Assert statements added to ensure requisite info present before POSTing to GCP
- Re-worked vignette validation functionality
	+ Clarified language returned by LDT to tell user validation is only against expected vignette content pairings, not validating overall message in some way.
- Refactored repo_test function
	+ Removed repeat code blocks to allow for implementation of single repo test function

## Version 1.4.1
Released 8/10/23
- Changed `LDT_Addendum`
	+ Changed from checking persona based keys to staff_number based keys
	+ Allows for validation of any successful post request
- Changed validation procedure to allow any post request to be validated
	+ Implemented validation of post request(s) based on using staff_number to compare against keys vs. using personas
	+ Successfully tested functionality with both CSV and GitHub input messages

## Version 1.4.0
Released 8/9/23
- Added `LDT_Addendum.py` to Leakdown Tester folder
	+ Functions as a store for large text variables that may need to periodically change without impacting `leakTester.py`
	+ Contains validation target values
	+ Contains header and footer of input_message JSON content for CSV payload building
- Removed function `assemble_payload`
	+ Obsolete with LDT_Addendum addition	
- Added `validate` functionality to `repoTest`
	+ Compares against a seperate python dictionary file with desired output message value pairs determined by the vignettes. Note: Only works alongside `repoTest`.
		* This file can be updated if vignette data changes without versioning Leakdown Tester

## Version 1.3.0
Released 8/9/23
- Added automated knowledgebase repo testing functionality
	+ use `--repoTest` as arg to run
- Refactored script for readability and cohesion
	+ GCP functionality not verified online
	+ Planned: Verified GCP functionality, anticipated in next patch (V 1.3.1)
- Reformatted CSV-JSON builder
	+ Removed debug key
	+ Updated exepected performance data headers
	+ Updated braketing to support debug key removal

## Version 1.2.0
Released 8/7/23
- Added Google Cloud Platform functionality
	+ use `--target cloud` to test against the GCP API instance
	+ Thanks Ayshwarya!

## Version 1.1.2
Release 8/2/23
- Updated useGit functionality
	+ GitHub links now supercede CSV content without user input
		* Changed warning print to INFO to reflect above
	+ useGit now accepts both 'raw' and standard github page links
- Updated startup messaging
	+ Welcome message now predecates all print statements
	+ Version number included in welcome message

## Version 1.1.1
Released 8/2/23
- Changed JSON content formatting for CSV-built messages
	+ Updated to new baseline being used for full-team pipeline testing

## Version 1.1.0
Released 8/2/23
- Implemented useGit functionality 
	+ Can now accept JSON content directly from GitHub files
	+ Requires raw github link
		* Planned: implement code to convert non-raw link to raw before import, with a checker so both can be acceptable

## Version 1.0.1
Released 7/30/23
- Published to GitHub
- Added environment variable functionality
- Added argument functionality
- Added response printing and saving
- Created user manual
