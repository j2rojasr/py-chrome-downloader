
# Download Chrome and Chrome Driver

A Python script that allows selecting a specific version of Google Chrome and downloading its respective Chrome and Chrome Driver files. It utilizes version information provided by the [GoogleChromeLabs](https://github.com/GoogleChromeLabs/chrome-for-testing) repository, specifically from various endpoints of their JSON API to fetch available versions and their download URLs.

## Usage

The script is interactive and guides the user through a menu to select the desired Chrome version and platform. It can be particularly useful for automated testing where a specific version of Chrome or its driver is required.

## Features

- Interactive selection of Chrome version and platform.
- Automated downloading of the selected file.
- File availability verification before downloading.

## API Information Used

This project utilizes several API endpoints provided by GoogleChromeLabs, such as:

- `known-good-versions.json`: Versions for which all Chrome for Testing (CfT) assets are available for download.
- `last-known-good-versions-with-downloads.json`: The latest versions for which all CfT assets are available for download across Chrome release channels (Stable/Beta/Dev/Canary), with an additional downloads property for each channel, listing the complete download URLs per asset.

## Installation

To install the necessary dependencies for this project, ensure Python is installed on your system and then execute the following command:


```
pip install -r requirements.txt
```

### Script Execution

Once the dependencies are installed, you can run the script:

```
python src/main.py
```

## License

MIT