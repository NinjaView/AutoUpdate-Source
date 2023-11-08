# NinjaView Auto-Updater Script

This script is designed to automatically update the NinjaView application on Windows. It checks for the latest version of the app, downloads it if available, and replaces the old executable while preserving user settings.

## Features

- Automatic version checking against a remote server
- Secure downloading of the new version over HTTPS
- Silent replacement of the old version
- Error handling and logging for troubleshooting
- Custom alert dialogs to inform users of updates

## Usage

Before running the script, ensure that Python and all required packages are installed on your system. The script uses `ctypes`, `win32api`, `http.client`, and `packaging.version`.

### Steps to Run the Updater

1. Create A New Folder called "updater" in the same folder as NinjaView.exe.
2. Place the script in the "updater" directory.
3. Execute the script using Python:

```
python updater.py
```

### Compile the updater
```
pip install pyinstaller
cd path\to\your\script
pyinstaller --onefile updater.py
```


## The script will perform the following actions:

Determine the current version of NinjaView installed.
Check for updates by contacting https://ninja-view.com/current_version.txt.
If a new version is available, it will notify the user and initiate the download process.
Once the new version is downloaded, it will replace the old executable with the new one.
It will clean up any temporary files if necessary.
Requirements
Python 3.x
Windows Operating System
Internet Connection
The packaging Python module, which can be installed via pip with pip install packaging
Configuration
No additional configuration is required. However, ensure that the URLs within the script are correct and pointing to your update server.

## Handling Executables
The script assumes that the executable has a standard naming convention (NinjaView.exe). If your executable follows a different naming pattern, you will need to adjust the script accordingly.

## Notifications
Alert dialogs will appear to notify the user when an update is available and when the update process is complete.

## Error Handling
The script contains basic error handling for common issues such as network errors, file access issues, and update mismatches. Detailed errors will be printed to the console.

## Contributing
If you'd like to contribute to the development of this auto-updater script, please follow the standard GitHub fork & pull request workflow.

## Support
If you encounter any problems or have questions, please file an issue on this GitHub repository.
