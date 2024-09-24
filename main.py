import pathlib
import tempfile

import lib.downloader
import lib.excel_processor
import lib.scraper
import lib.webdrivermanager




if __name__ == "__main__":
    # Initialize WebDriverManager
    driver_manager = lib.webdrivermanager.WebDriverManager()
    driver = driver_manager.get_driver()

    try:
        # Initialize Scraper
        scraper = lib.scraper.Scraper(driver)

        # Navigate to the target page
        scraper.navigate_to_page("https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html")
        scraper.remove_cookie_banner()

        # Click the necessary elements to reach the download links
        scraper.click_element("Censos")
        scraper.click_element("Censos/Censo_Demografico_1991")
        scraper.click_element("Censos/Censo_Demografico_1991/Indice_de_Gini")

        # Get download links
        download_links = scraper.get_download_links("//*[@id='Censos/Censo_Demografico_1991']//ul[@role='group']", 
                                                    "https://ftp.ibge.gov.br/Censos/Censo_Demografico_1991/Indice_de_Gini/")
    finally:
        # Ensure the WebDriver quits properly
        driver_manager.quit()


    # Create a temporary directory to store downloaded Zip files
    with tempfile.TemporaryDirectory() as tmp:
        temp_dir = pathlib.Path(tmp)
        extracted_files_dir = temp_dir / "extracted"
        downloader = lib.downloader.Downloader(temp_dir)

        # Download Zip files
        for link in download_links:
            downloader.download_file(link)

        # Extract Zip files
        for zip_file in temp_dir.glob("*.zip"):
            downloader.extract_zip_file(pathlib.Path(zip_file), extracted_files_dir)

        # Set the database where the data will be stored
        db_path = pathlib.Path("/clever/db/data.db")
        processor = lib.excel_processor.ExcelProcessor(db_path, table_name="DemographicCensus1991")
        processor.create_table()

        # Process extracted Excel files and fill in the database
        for filename in extracted_files_dir.glob("*.XLS"):
            processor.process_excel_file(extracted_files_dir / filename)