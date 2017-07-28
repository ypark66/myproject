import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.select import Select
import smtplib
from email.mime.text import MIMEText

# from selenium.webdriver.support.ui import Select



"""
auto.py
This script aims for students in University of Illnois at Urbana-Champaign.
Support registering to unlimited number of classes
TO DO.
1. download geckodriver and Firefox browser
2. type the directory to the geckodriver.exe at "webdriver.Firefox(executable_path=r"
User needs to fill out the variable in fill out area and modify the index for list access.
Set the refresh rate at "time.sleep("

Functions:  navigate to the registration, auto register the course

Caution: Logging into the account that is currently being used by this program 
           will cause error and delay the registration process

created by Yeongyoon Park on 2017-07-24
Copyright (c) 2017 Yeongyoon Park. All rights reserved.

"""

#fillout area
username='ypark66'
password='shibalPW12!'
course_num = ['446', '391','411']
course_section_num = ['46792','47765','30109']                   #enter the CRN for section and discussion numbers
course_discussion_num = [[],[47766],[]]
self_service = 'https://apps.uillinois.edu/selfservice/'      #URL to self service
semester = 'Fall 2017 - Urbana-Champaign'                     #check the right word from options in html
major = ['Computer Science', 'Electrical and Computer Engr', 'Computer Science']
from_this_email = 'ypark66@fasoo.com'
email_address = 'dusrbs@gmail.com'
isFirst = True
"""
     Navigate the self service page and log in to UIUC page
     @param username
     @param password
     @param self_service URL to U of I self service page
     @return driver
"""
def log_in(driver, username, password, self_service):
    url = self_service
    if driver == 0:
        driver = webdriver.Firefox(executable_path=r'C:\Users\fasoo-03\gecko\geckodriver.exe')
        #driver = webdriver.Chrome(executable_path=r'C:\Users\fasoo-03\gecko\chromedriver.exe')
        isFirst = True
    else:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
        driver.switch_to.window(driver.window_handles[-1])
        wait = WebDriverWait(driver, 100)
        wait.until(EC.title_contains('New Tab'))
        isFirst = False
    driver.get(url)
    driver.find_element_by_link_text('University of Illinois at Urbana-Champaign (URBANA)').click()
    if (isFirst):
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.NAME,"inputEnterpriseId")))
        user_field = driver.find_element_by_name("inputEnterpriseId")
        password_field = driver.find_element_by_name("password")
        user_field.clear()
        password_field.clear()
        user_field.send_keys(username)
        password_field.send_keys(password)
        driver.find_element_by_name("BTN_LOGIN").click()
    return driver


"""
     Navigate the main menu and gets the Course Search page of the given values
     @param   driver main menu
     @param   major  major of the course to be searched
     @param   semester semester to be searched
     @return  curr_page the page source
     @return  driver
"""
def navigate(driver, username, password, major, semester=None):
    driver = log_in(driver, username, password, self_service)
    print('LOG IN SUCCESSFUL')
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Registration")))
    driver.find_element_by_partial_link_text("Registration").click()
    if logged_out_check(driver):
        print('Logged out during Entering Classic Registration & Records')
        return None,None
    print('Entering Classic Registration & Records Successful')

    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Classic")))
    driver.find_element_by_link_text('Classic Registration').click()
    if logged_out_check(driver):
        print('Logged out during Entering Classic Registration')
        return None,None
    print('Entering Classic Registration Successful')

    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Look-up or Select")))
    driver.find_element_by_link_text('Look-up or Select Classes').click()
    if logged_out_check(driver):
        print('Logged out during Entering Look-up or Select Classes')
        return None,None
    print('Entering Look-up or Select Classes Successful')

    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"I Agree to the Above")))
    driver.find_element_by_link_text('I Agree to the Above Statement').click()
    if logged_out_check(driver):
        print('Logged out during Entering Agree Terms')
        return None,None
    print('Agree Terms Successful')

    #semester
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.ID,'term_input_id')))
    options = Select(driver.find_element_by_id('term_input_id'))
    options.select_by_visible_text(semester)
    path = '//input[@type="submit" and @value="Submit"]'
    driver.find_element_by_xpath(path).click()
    if logged_out_check(driver):
        print('Logged out during Selecting Semesters')
        return None,None
    print('Selecting Semesters Successful')

    #major
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.XPATH,'//select[@name="sel_subj" and @size="10"]')))
    path = '//select[@name="sel_subj" and @size="10"]'
    options = Select(driver.find_element_by_xpath(path))
    options.select_by_visible_text(major)
    path = '//input[@type="submit" and @value="Course Search"]'
    driver.find_element_by_xpath(path).click()
    if logged_out_check(driver):
        print('Logged out during Selecting major')
        return None,None
    print('Selecting {0} Major Successful'.format(major))
    curr_page = driver.page_source
    return curr_page, driver


"""
    finds the index of the course from parsed Look-Up or Select Classes Results page
    @param course_num course to register
    @param soup parsed page
    @return main_page_idx index
"""
def find_course_position(course_num, soup, main_page_idx):
    idx = 0
    for course in soup('td', class_='dddefault', attrs={"width": "10%"}):
        if course_num == course.string:
            main_page_idx = idx
            break
        idx += 1
    return main_page_idx


"""
    Check whether the sections are full. Skip discussion if empty
    @param soup Parsed Look-up Result page 
    @param course_section_num
    @param course_discussion_num
    @return false if courses are full, none if CRN is invalid
"""
def check_full_or_not(soup, course_section_num, course_discussion_num, index):
    course_section_num_idx = find_section_num_idx(soup, course_section_num)
    if course_section_num_idx == None:
        print('{0} is an invalid section number'.format(course_section_num))
        return None
    course_full_or_not_indicator = soup('a', string=re.compile('\d+'))[course_section_num_idx].parent.find_previous('td').string

    if len(course_discussion_num)!=0:
        flag = True
        idx = 0
        delIdx = []
        Discussion_is_available = False

        for discussion in course_discussion_num:
            discussion_section_num_idx = find_section_num_idx(soup, discussion)
            if discussion_section_num_idx != None:
                if soup('a', string=re.compile('\d+'))[discussion_section_num_idx].parent.find_previous('td').string != 'C':
                    Discussion_is_available = True
                    index.append(idx)
                    flag = False
            else:
                print('{0} is an invalid discussion CRN. It will be deleted from the discussion list'.format(discussion))
                delIdx.append(idx)
            idx += 1

        if len(delIdx) != 0 and flag:
            delIdx.reverse()
            for index in delIdx:
                del course_discussion_num[index]
        if len(course_discussion_num)==0:
            print("All of the discussion CRNs are invalid")
            return None         #all discussion section numbers are invalid
    else:
        return course_full_or_not_indicator != 'C'
    return course_full_or_not_indicator != 'C' and Discussion_is_available


"""
    finds the index of the given CRN
"""
def find_section_num_idx(soup, crn):
    section_num_idx = 0
    for section in soup('a', string=re.compile('\d+')):
        if str(crn) == section.string:
            return section_num_idx
        section_num_idx += 1
    return None


def register(driver, index, course_section_num, course_discussion_num):
    print(' start register!')
    driver.find_element_by_xpath('//input[@value="Register"]').click()
    crn_blank1 = driver.find_element_by_xpath('//input[@id="crn_id1"]')
    crn_blank1.send_keys(course_section_num)

    if len(index) >= 1:                                                  ### later add time conflict resolver
        crn_blank2 = driver.find_element_by_xpath('//input[@id="crn_id2"]')
        crn_blank2.send_keys(course_discussion_num[index[0]])

    driver.find_element_by_xpath('//input[@value="Submit Changes"]').click()
    print(' success !')
    print(' please check any warnings ')


def send_notification(major, course_number):
    msg = MIMEText('Registration for {0} {1} is ready'.format(major,course_number))

    msg['Subject'] = 'Course Registration Success'
    msg['From'] = from_this_email
    msg['To'] = email_address

    s = smtplib.SMTP('localhost')
    s.sendmail(from_this_email, [email_address], msg.as_string())
    s.quit()


"""
    deletes course info that has been successfully registered
    @param i index to be deleted
"""
def delete_info(i):
    course_section_num.pop(i)
    course_discussion_num.pop(i)
    course_num.pop(i)
    major.pop(i)


"""
    check if the account is logged out for some reason
    @param driver webdriver object
"""
def logged_out_check(driver):
    #time.sleep(1)     #if user wants to run this program without stopping, set this number based on internet speed
    if driver.current_url == 'https://apps.uillinois.edu/selfservice/error/':
        return True
    else:
        return False


def main():
    main_page_idx_offset = 3
    main_page_idx_submit_button_idx = 3
    main_page_idx = 0                       #index of the course number
    check = False
    soup = [0]*len(course_num)
    driver = 0
    while True:
        if len(course_num) <= 0:
            break
        retry = False
        i = 0
        while i < len(course_num):
            print('------------------Working on {0}th tab for {1} {2} {3} course registration------------------'.format(i+1,semester, major[i], course_num[i]))
            curr_page, driver = navigate(driver, username,password, major[i], semester)
            if driver == None: #logged out during navigation
                print('Wait and restart the program')
                driver.quit()
                driver = 0
                time.sleep(10)
                break
            soup[i] = bs(curr_page, 'html.parser')
            main_page_idx = find_course_position(course_num[i], soup[i], main_page_idx)
            main_page_idx += main_page_idx_offset
            path = "//table[@summary='This layout table is used to present the course found']/tbody/tr[%s]/td[%s]/form/input[@type='submit']" % (main_page_idx, main_page_idx_submit_button_idx)
            driver.find_element_by_xpath(path).click()
            print("Entered Look-Up or Select Classes Result")
            i+=1
            time.sleep(3)

            #check whether the courses are full. if not register
        while True:
            i=0
            check = False
            if retry == True:   #if failure occured, restart the program
                break
            if len(course_num) <= 0:  #if registeration is finished, end the program
                break
            while i < len(course_num):
                #For all courses in list, check whether the course is full
                driver.switch_to.window(driver.window_handles[i])
                print('-----Look up for {0} {1} {2} course registration on {3}th tab-----'.format(semester, major[i],
                                                                                        course_num[i], i+1))
                driver.refresh()
                try :
                    driver.switch_to_alert().accept()
                except NoAlertPresentException:   #logged out for some reason. wait and restart the program
                    retry = True
                    print('Logged out during look-up phase... Restart the program')
                    driver.quit()
                    driver = 0
                    time.sleep(300)
                    break
                curr_page = driver.page_source
                soup[i] = bs(curr_page, 'html.parser')
                index = []
                check = check_full_or_not(soup[i], course_section_num[i], course_discussion_num[i], index)
                if check == None:
                    print("Invalid. Change the CRN. Deleting the course from list")    #what if all the discussions were deleted for the class that requires discussion?
                    delete_info(i)
                    driver.close()
                    break

                # Course ready, start register
                elif check == True:
                    break

                #Course is full. Wait and check again
                print('{0} {1} right now is full.   {2}'.format(major[i], course_num[i], time.strftime("%Y-%m-%d %H:%M.%S")))
                print('waiting.......')
                time.sleep(5)                              #rate of refreshing the website by seconds
                i+=1

            if check == True:
                register(driver, index, course_section_num[i], course_discussion_num[i])
                send_notification(major[i], course_section_num[i])
                delete_info(i)

    return
if __name__ == "__main__":
    main()

