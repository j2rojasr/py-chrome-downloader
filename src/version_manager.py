import inquirer
from downloader import make_request, check_url_availability
from url_constructor import build_chrome_url


def get_versions_and_subversions():
    chrome_versions_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions.json"

    try:
        response = make_request(chrome_versions_url)
        if response is None:
            return None

        data = response.json()

        print("Available Chrome versions:")

        # get the main versions of Chrome
        versions_data = data["versions"]
        main_versions = set()

        for version_data in versions_data:
            full_version = version_data["version"]
            main_version = full_version.split(".")[0]
            main_versions.add(main_version)

        main_versions_sorted = sorted(main_versions)

        # use inquirer for terminal usability
        main_version_question = inquirer.List('main_version',
                                              message="Select a main version:",
                                              choices=main_versions_sorted)
        main_version_response = inquirer.prompt([main_version_question])

        if main_version_response is None:
            print("No version selected. Aborting...")
            return None

        selected_main_version = main_version_response['main_version']

        # filter available subversions based on the selected main version
        available_subversions = set()
        for version in versions_data:
            if version["version"].startswith(f"{selected_main_version}."):
                available_subversions.add(version["version"])
        print("\nAvailable subversions:")

        subversion_question = inquirer.List('subversion',
                                            message="Select a subversion:",
                                            choices=available_subversions)
        subversion_response = inquirer.prompt([subversion_question])

        if subversion_response is None:
            print("No subversion selected. Aborting...")
            return None

        selected_subversion = subversion_response['subversion']

        return selected_subversion

    except Exception as e:
        print(f"Error obtaining Chrome versions: {e}")
        return None, None


def get_platform():
    print("\nAvailable platforms:")
    platform_options = [
        {"name": "Linux 64-bit", "value": "linux64"},
        {"name": "Mac ARM64", "value": "mac-arm64"},
        {"name": "Mac x64", "value": "mac-x64"},
        {"name": "Windows 32-bit", "value": "win32"},
        {"name": "Windows 64-bit", "value": "win64"}
    ]

    platform_names = [option['name'] for option in platform_options]

    platform_question = inquirer.List('platform',
                                      message="Select a platform:",
                                      choices=platform_names)

    platform_response = inquirer.prompt([platform_question])

    if platform_response is None:
        print("No platform selected. Aborting...")
        return None

    selected_platform_name = platform_response['platform']

    selected_platform = None

    for option in platform_options:
        if option['name'] == selected_platform_name:
            selected_platform = option['value']
            break

    return selected_platform


def select_files_to_download(version, platform):
    file_options = [
        {
            "name": "Chrome",
            "value": {
                "type": "chrome",
                "url": ""
            }
        },
        {
            "name": "Chrome Driver",
            "value": {
                "type": "chromedriver",
                "url": ""
            }
        },
    ]

    for option in file_options:
        file_type = option["value"]["type"]
        file_url = build_chrome_url(version, platform, file_type)
        option["value"]["url"] = file_url

        option_text = option["name"]
        if check_url_availability(file_url):
            option["name"] = f"{option_text} (✅)"
        else:
            option["name"] = f"{option_text} (❌)"

    file_question = inquirer.Checkbox('files_to_download',
                                      message="Select the files you wish to download:",
                                      choices=[opt['name'] for opt in file_options])
    file_response = inquirer.prompt([file_question])

    if file_response is None:
        print("No files selected. Aborting...")
        return None

    selected_files = file_response['files_to_download']

    selected_urls = []

    for option in file_options:
        for file in selected_files:
            if option['name'] == file:
                selected_urls.append(option["value"]["url"])
                break

    return selected_urls
