def build_chrome_url(version, platform, type):
    type_formatted = type.lower().replace(" ", "")

    if type_formatted == 'chrome':
        url_template = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/{platform}/chrome-{platform}.zip"
    elif type_formatted == 'chromedriver':
        url_template = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/{platform}/chromedriver-{platform}.zip"
    else:
        raise ValueError(
            "Invalid type. It must be 'chrome' or 'chromedriver'.")

    final_url = url_template.format(version=version, platform=platform)
    return final_url
