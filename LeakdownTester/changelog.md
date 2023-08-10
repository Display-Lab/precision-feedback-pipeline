# Changelog for Leakdown Tester Script
## Version 1.4.1
Released 8/10/23
- Changed `LDT_Addendum`
	+ Changed from checking persona based keys to staff_number based keys
	+ Allows for validation of any successful post request
- Changed validation procedure to allow any post request to be validated
	+ Implemented validation of any post request based on using staff_number to compare against keys vs. using personas
	+ Tested functional with CSV and GitHub messages

## Version 1.4.0
Released 8/9/23
- Added `LDT_Addendum.py` to Leakdown Tester folder
	+ Functions as a store for large text variables that may need to periodically change without impacting `leakTester.py`
	+ Contains validation target values
	+ Contains header and footer of input_message JSON content for CSV payload building
- Removed function `assemble_payload`
	+ Obsolete with LDT_Addendum addition	
- Added `validate` functionality to `repoTest`
	+ Compares against a seperate python dictionary file with desired output message value pairs determined by the vignettes.
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
