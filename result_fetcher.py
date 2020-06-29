from selenium import webdriver
import re
import csv

options = webdriver.chrome.options.Options()
options.headless = True
driver=webdriver.Chrome(executable_path="C:\ChromeDriver\chromedriver.exe", options=options)
driver.get("http://136.232.2.202:8084/student20o.aspx")

with open('results.csv', 'w') as result_file:
    fieldnames = ['Roll', 'Name', 'SGPA']
    csv_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    for roll in range(12618001001, 12618001050):
        
        driver.find_element_by_name('roll').send_keys(roll)
        driver.find_element_by_name('sem').send_keys(3)
        driver.find_element_by_name('Button1').click()
            
        try:
            sgpa_text = driver.find_element_by_id('lblbottom1').text
            name_text = driver.find_element_by_id('lblname').text
            
            sgpa_pattern = re.compile(r'([0-9]+\.[0-9]+)')
            name_pattern = re.compile(r'(Name  )([A-Z ]+)') 
            sgpa = re.search(sgpa_pattern, sgpa_text).group(0)
            name = re.search(name_pattern, name_text).group(2)
            print(roll, name, sgpa)
            csv_writer.writerow({'Roll': roll, 'Name': name, 'SGPA': sgpa})
        except Exception:
            print(roll, "404: Not Found Result")
            pass
        driver.back()
driver.close()
