# Changelog for Leakdown Tester Script
## Version 1.3.0
Released 8/9/23
- Added automated knowledgebase repo testing functionality
	+ use `--repoTest` as arg to run
- Refactored script for readability and cohesion
	+ GCP functionality not verified online, releasing dev build as 1.3.0 to add tested GCP func. in patch (V 1.3.1)
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
