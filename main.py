from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import csv
from pathlib import Path

url = "https://smabali.spmb.id/010101/hasil"
selected_school = []
selection_type = "Domisili"

def main():

    options = webdriver.EdgeOptions()
    driver = webdriver.ChromiumEdge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    
    driver.get(url)
    school_data = []
    school_page = 1

    while True:
        print(f"--- Processing School Page {school_page} ---")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.p-datatable-tbody tr.p-datatable-selectable-row"))
        )
        
        sch_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.p-datatable-tbody tr.p-datatable-selectable-row")
        rows_count = len(sch_rows)

        for i in range(rows_count):
            current_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.p-datatable-tbody tr.p-datatable-selectable-row")
            row = current_rows[i]

            school_name = row.find_element(By.XPATH, "./td[1]/div/div[1]").text.strip()
            npsn_text = row.find_element(By.XPATH, "./td[1]/div/div[2]").text.strip()
            npsn = npsn_text.split("-")[-1].strip() if "-" in npsn_text else npsn_text
            highest_val = row.find_element(By.XPATH, "./td[2]//div[contains(@class, 'bg-green-50')]/span").text.strip()
            lowest_val = row.find_element(By.XPATH, "./td[2]//div[contains(@class, 'bg-red-50')]/span").text.strip()

            data = {
                "school_name": school_name,
                "npsn": npsn,
                "highest": highest_val,
                "lowest": lowest_val
            }

            school_data.append(data)

            if school_name not in selected_school: continue
            selected_school.remove(school_name)

            clickable_target = row.find_element(By.XPATH, "./td[1]/div/div[1]")
            current_url = driver.current_url
            driver.execute_script("arguments[0].click()", clickable_target)
            WebDriverWait(driver, 10).until(EC.url_changes(current_url))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.p-datatable-tbody tr"))
            )
            students_data = []
            student_page = 1

            while True:
                print(f"--- Processing Student Page {student_page} ---")

                student_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.p-datatable-tbody tr")
                student_rows_count = len(student_rows)
                for j in range(student_rows_count):
                    print("student", j)
                    current_rows = driver.find_elements(By.CSS_SELECTOR, "tbody.p-datatable-tbody tr")
                    row = current_rows[j]

                    student_link = row.find_element(By.XPATH, "./td[3]/span/a[@class='text-blue-600']")
                    current_url = driver.current_url
                    driver.execute_script("arguments[0].click()", student_link)
                    WebDriverWait(driver, 10).until(EC.url_changes(current_url))
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.font-semibold"))
                    )

                    student_name = driver.find_element(By.CSS_SELECTOR, "h1.font-semibold").text.strip()
                    smp_origin = driver.find_element(By.CSS_SELECTOR, "div.text-base.text-slate-600").text.strip()
                    nisn_text = driver.find_element(
                        By.XPATH, "//span[text()='NISN Murid SPMB']/ancestor::div[contains(@class,'flex')]/div[2]"
                    ).text.strip()
                    nisn = nisn_text.split("\n")[-1].strip()
                    math_score_text = driver.find_element(
                        By.XPATH, "//span[contains(text(),'TKA Matematika')]/ancestor::div[contains(@class,'flex')]/div[2]"
                    ).text.strip()
                    math_score = math_score_text.split('\n')[-1].strip()
                    indonesian_score_text = driver.find_element(
                        By.XPATH, "//span[contains(text(),'TKA Bahasa Indonesia')]/ancestor::div[contains(@class,'flex')]/div[2]"
                    ).text.strip()
                    indonesian_score = indonesian_score_text.split("\n")[-1].strip()

                    student_details = {
                        "name": student_name,
                        "origin_smp": smp_origin,
                        "nisn": nisn,
                        "math": math_score,
                        "indonesian": indonesian_score
                    }
                    print(student_details)
                    students_data.append(student_details)
                    driver.back()

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button.p-paginator-next")

                    is_disabled_attr = next_button.get_attribute("disabled") is not None
                    is_disabled_class = "p-disabled" in next_button.get_attribute("class")

                    if is_disabled_attr or is_disabled_class:
                        print("Reached the last student page. Scraping complete!")
                        break
                    
                    driver.execute_script("arguments[0].click();", next_button)
                    student_page += 1

                    WebDriverWait(driver, 5).until(EC.staleness_of(student_rows[0]))
                
                except (TimeoutException, NoSuchElementException):
                    print("Next button not found or page timeout. Stopping.")
                    break
            
            save_result(school_name, students_data)

            driver.back()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.p-datatable-tbody tr.p-datatable-selectable-row"))
            )


        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button.p-paginator-next")

            is_disabled_attr = next_button.get_attribute("disabled") is not None
            is_disabled_class = "p-disabled" in next_button.get_attribute("class")

            if is_disabled_attr or is_disabled_class:
                print("Reached the last page. Scraping complete!")
                break
            
            driver.execute_script("arguments[0].click();", next_button)
            school_page += 1

            WebDriverWait(driver, 5).until(EC.staleness_of(sch_rows[0]))
        
        except (TimeoutException, NoSuchElementException):
            print("Next button not found or page timeout. Stopping.")
            break
    
    save_result(f'Seleksi {selection_type}', school_data)
    driver.quit()
    print("Scraping success!")

def save_result(filename, result):
    keys = result[0].keys()
    directory = Path(selection_type)
    directory.mkdir(parents=True, exist_ok=True)
    
    with open(f"{selection_type}/{filename}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(result)
    print(f"{filename}.csv saved successfully!")

if __name__ == "__main__":
    main()
