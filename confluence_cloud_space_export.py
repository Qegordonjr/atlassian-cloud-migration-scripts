import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuration
confluence_base_url = 'https://yourdomain.atlassian.net/wiki'
download_directory = 'path/to/download/directory'

# Ensure the download directory exists
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Set up Chrome options to automatically download files to the specified directory
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_directory,
    'download.prompt_for_download': False,
    'directory_upgrade': True,
})

# Initialize the WebDriver using Selenium Manager
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 60)

# Function to export a space as XML
def export_space(space_key):
    try:
        # Navigate to the space export page for XML export
        export_url = f'{confluence_base_url}/spaces/exportspacexml.action?key={space_key}'
        driver.get(export_url)
        print(f'Navigated to: {export_url}')
        
        # Wait for manual login if necessary
        print("Please log in to Confluence if not already logged in. Press Enter here when done.")
        input("Press Enter after logging in and navigating back to the export page...")

        # Wait until the page is fully loaded
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print('Page loaded.')

        # Debugging: Print out the page source for manual inspection
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print('Saved page source to page_source.html.')

        # Click the Export button using a CSS selector
        export_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.submit[type='submit'][name='confirm'][value='Export']")))
        print('Export button found.')
        export_button.click()
        print('Clicked Export button.')
        
        print(f'Started XML export for space {space_key}. Please monitor the Confluence UI for export progress and download the file manually if necessary.')
        
    except Exception as e:
        print(f"Error exporting space {space_key}: {e}")

# Main script execution
if __name__ == "__main__":
    space_key = 'BD'  # Replace with the actual space key you want to export
    export_space(space_key)
    print("Export process initiated. Press Enter to close the browser.")
    input()  # Wait for user input before closing the browser
    driver.quit()
