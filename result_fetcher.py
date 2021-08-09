# Selenium program to fetch result of all students of HIT-K

from selenium import webdriver
import re
import csv


def csv_maker(data):    # take all the results and put it in a csv
    with open('results.csv', 'w') as result_file:
        fieldnames = ['Roll', 'Name', 'SGPA']
        csv_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for person_data in data:
            csv_writer.writerow(
                {'Roll': person_data[0], 'Name': person_data[1], 'SGPA': person_data[2]})


def get_data(sem, site, low_roll, high_roll):   # fetch results and return 2d list of data
    data = []
    options = webdriver.chrome.options.Options()
    options.headless = True
    driver = webdriver.Chrome(
        executable_path="C:\ChromeDriver\chromedriver.exe", options=options)
    driver.get(site)

    with open('results.csv', 'w') as result_file:

        for roll in range(low_roll, high_roll):

            driver.find_element_by_name('roll').send_keys(roll)
            driver.find_element_by_name('sem').send_keys(sem)
            driver.find_element_by_name('Button1').click()

            try:
                sgpa_text = driver.find_element_by_id('lblbottom1').text
                name_text = driver.find_element_by_id('lblname').text

                sgpa_pattern = re.compile(r'([0-9]+\.[0-9]+)')
                name_pattern = re.compile(r'(Name  )([A-Z ]+)')
                sgpa = re.search(sgpa_pattern, sgpa_text).group(0)
                name = re.search(name_pattern, name_text).group(2)

                print(roll, name, sgpa)

                person_data = [roll, name, sgpa]
                data.append(person_data)
            except Exception:
                print(roll, "404: Not Found Result")

            driver.back()
    driver.close()
    return (sorted(data, key=lambda x: x[2], reverse=True))


if __name__ == "__main__":
    sem = int(input("Enter semester: "))
    site = input("Enter latest result site: ")
    low_roll, high_roll = map(int, input("Enter roll number range: ").split())

    choice = input("Do you want to save the data in CSV? (y/n) ")

    data = get_data(sem, site, low_roll, high_roll+1)

    if(choice == 'y'):
        csv_maker(data)
