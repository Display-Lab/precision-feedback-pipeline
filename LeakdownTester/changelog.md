# Changelog for Leakdown Tester Script
## Version 1.2.0
Released 8/7/23
- Added Google Cloud Platform functionality
	+ Thanks Ayshwarya!

## Version 1.1.2
Release 8/2/23
- Updated useGit functionality
	+ GitHub links now supercede CSV content without user input
		* Changed warning print to INFO to reflect above
	+ useGit now accepts raw and normal github page links
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
	+ Now can accept JSON content directly from GitHub files
	+ Requires raw github link
		* planning to implement some code to convert non-raw link to raw before import, with a checker so both can function properly.

## Version 1.0.1
Released 7/30/23
- Added environment variable functionality
- Added argument functionality
- Added response printing and saving
- Created user manual
