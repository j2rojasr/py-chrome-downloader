from downloader import download_selected_files
from version_manager import get_platform, get_versions_and_subversions, select_files_to_download


def main():
    version = get_versions_and_subversions()

    if version:
        platform = get_platform()

        archivos_a_descargar = select_files_to_download(
            version, platform)

        download_selected_files(archivos_a_descargar)


if __name__ == "__main__":
    main()
