import os
import sys
import time
import logging
import http.client
import ctypes
from win32api import GetFileVersionInfo, LOWORD, HIWORD
from urllib.parse import urlparse
from packaging import version

def alert(title, text, style):
    # Styles:
    # 0 : OK
    # 1 : OK | Cancel
    # 2 : Abort | Retry | Ignore
    # 3 : Yes | No | Cancel
    # 4 : Yes | No
    # 5 : Retry | No 
    # 6 : Cancel | Try Again | Continue
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def get_file_version(filename):
    """
    Extracts the product version number from a file's metadata on Windows.
    """
    try:
        if not os.path.exists(filename):
            print(f"The file {filename} does not exist")
            return None

        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{HIWORD(ms)}.{LOWORD(ms)}.{HIWORD(ls)}.{LOWORD(ls)}"
        return version
    except Exception as e:
        print(f"Cannot get version for {filename}: {e}")
    return None

def get_updater_directory():
    # This function will now return the directory of the updater script itself
    if getattr(sys, 'frozen', False):
        # If the application is frozen using a tool like cx_Freeze or PyInstaller
        updater_path = sys.executable
    else:
        # If it's a script file
        updater_path = os.path.abspath(__file__)
    return os.path.dirname(updater_path)

def get_http_connection(url):
    url_parts = urlparse(url)
    conn = http.client.HTTPSConnection(url_parts.netloc) if url_parts.scheme == 'https' else http.client.HTTPConnection(url_parts.netloc)
    return conn

def check_for_update(local_version, version_url):
    try:
        conn = get_http_connection(version_url)
        url_parts = urlparse(version_url)
        conn.request("GET", url_parts.path)
        response = conn.getresponse()
        
        if response.status == 200:
            current_version = response.read().decode().strip()
            print(f"Local version: {local_version}, Current version: {current_version}")  # For debugging
            if version.parse(current_version) > version.parse(local_version):
                return current_version
    except Exception as e:
        print(f"Error checking for update: {e}")
    finally:
        conn.close()
    return None

def download_new_version(new_version, download_url):
    try:
        conn = get_http_connection(download_url)
        url_parts = urlparse(download_url)
        conn.request("GET", url_parts.path)
        response = conn.getresponse()
        
        if response.status == 200:
            update_file_path = os.path.join(get_updater_directory(), f"NinjaView_v{new_version}.exe")
            with open(update_file_path, 'wb') as file:
                file.write(response.read())
            return update_file_path
    except Exception as e:
        print(f"Error downloading new version: {e}")
    finally:
        conn.close()
    return None

def replace_old_executable(update_file_path, app_dir):
    current_executable_path = os.path.join(app_dir, "NinjaView.exe")
    old_executable_path = os.path.join(app_dir, "NinjaView_old.exe")

    try:
        # Rename the current executable to mark it as old
        if os.path.exists(current_executable_path):
            os.rename(current_executable_path, old_executable_path)
            print("Current version renamed to old version.")

        # Check if the update was downloaded successfully
        if not os.path.exists(update_file_path):
            print("Update file not found, aborting replacement.")
            return

        # Rename the downloaded update to the main executable
        os.rename(update_file_path, current_executable_path)
        print("Updated version set as current executable.")
        
        # After the new executable is in place, remove the old one
        if os.path.exists(old_executable_path):
            os.remove(old_executable_path)
            print("Old version removed successfully.")

    except Exception as e:
        print(f"Failed to update executable: {e}")

    finally:
        # Clean up the downloaded file if it's still there
        if os.path.exists(update_file_path):
            try:
                os.remove(update_file_path)
                print("Downloaded update file removed successfully.")
            except Exception as e:
                print(f"Unable to remove downloaded update file: {e}")



def main():
    updater_dir = get_updater_directory()
    # Assuming the application directory is the parent directory of the updater's directory.
    app_dir = os.path.dirname(updater_dir)
    local_version = get_file_version(os.path.join(app_dir, "NinjaView.exe"))

    if local_version is None:
        print("Unable to determine the current local version of NinjaView.")
        sys.exit(1)

    version_url = "https://ninja-view.com/current_version.txt"
    new_version = check_for_update(local_version, version_url)

    if new_version:
        alert("Update Notification", "New version available: {}. Download update.".format(new_version), 0)

        print(f"New version available: {new_version}. Downloading update...")
        download_url = f"https://ninja-view.com/update/NinjaView_v{new_version}.exe"
        update_file_path = download_new_version(new_version, download_url)

        if update_file_path:
            print("Update downloaded. Updating application...")
            replace_old_executable(update_file_path, app_dir)  # Pass app_dir as an argument here
            alert("Update Notification", "Update Complete: {}. Running Latest Version".format(new_version), 0)
            #print("Update complete. You may now run the updated NinjaView.")
    else:
        print("You have the latest version of NinjaView.")

if __name__ == "__main__":
    main()
