from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException
import time
import sys
from selenium.webdriver import FirefoxProfile
from account_dat_creator import *
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

inst_g_v = "1.2" # File Version

if sys.version_info < (3, 6):
    print("Please execute again with Python 3.6 at least")
    sys.exit(0)
print("<<<<< Instagram Grabber " + inst_g_v + " >>>>>")
print("")
print("<<<<<<<<<< by Aspoky >>>>>>>>>>")
print("")
print("Type '1' to start or '2' to view help")
print("")
sl = input("")
if sl == '1':
    ua = UserAgent()
    global file1
    try:
        file1 = open("account.dat", "r")
        # Reading line
        for line in file1:
            # getting data
            fieldss = line.split(":")
            username11 = fieldss[0]
            pass22 = fieldss[1]
        file1.close()
        print("Logging...")
    except FileNotFoundError:
        print("account.dat not found")
        print("Create it!")
        username11 = input("User?: ")
        pass22 = input("Pass?: ")
        cr_mod_account(username11, pass22)

    #user_of_data = input("Username to get data? (if you dont want this, leave blank): ")
    #searchany = input("Want to use the search? (y/n): ")
    if username11 == "" or pass22 == "":
        sys.exit("Username or Password empty.")

    profile1 = webdriver.FirefoxProfile()
    profile1.set_preference("general.useragent.override", ua.random)
    driver = webdriver.Firefox(profile1)
    agent = driver.execute_script("return navigator.userAgent")

    def __init__(self, username11, pass22):
        self.username = username11
        self.password = pass22
    logged = "false"
    def login():
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(1.75)
        time.sleep(0.75)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(username11)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(pass22)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(1.5)
    login()

    try:
        driver.find_element_by_css_selector(".GNbi9")
        print("")
        print("Suspicious login :(")
        driver.quit()
    except NoSuchElementException:
        try:
            driver.find_element_by_id("slfErrorAlert")
            print("")
            print("Incorrect Password!")
            print("")
            s222 = input("Password?:")
            if s222:
                passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
                passworword_elem.clear()
                passworword_elem.send_keys(s222)
                passworword_elem.send_keys(Keys.RETURN)
            else:
                pass
        except NoSuchElementException:
            print("Logged!")
            logged = "true"

    try:
        driver.find_element_by_css_selector(".aOOlW.HoLwm").click()
    except NoSuchElementException:
        pass
        time.sleep(1.25)


    def get_data(user_of_data):
        if "," not in user_of_data:
            driver.get("https://www.instagram.com/" + user_of_data + "/")
            time.sleep(0.5)
            print("")
            a = []
            b = []
            try:
                driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                print("")
                print("User not found :(")
                print("")
                wwwa99 = input("Try other user? (y/n): ")
                if wwwa99 == "y" or wwwa99 == "Y" or wwwa99 == "yes" or wwwa99 == "Yes":
                    asz8 = input("Username to get data? (if you dont want this, leave blank): ")
                    if asz8:
                        get_data(asz8)
                else:
                    pass
            except NoSuchElementException:
                all_spans = driver.find_elements_by_css_selector('.g47SY')
                for span in all_spans:
                    b.append(span.get_attribute("title"))
                    a.append(span.text)
                time.sleep(0.5)
                if (b[1] == ""):
                    b[1] = a[1]
                print(user_of_data + "'s data")
                print("--------------------")
                print(a[0] + " posts")
                print(b[1] + " followers")
                print(a[2] + " following")
                print("--------------------")
                print("")
                wwwa = input("Get another user data? (y/n): ")
                if wwwa == "y" or wwwa == "Y" or wwwa == "yes" or wwwa == "Yes":
                    asz = input("Username to get data? (if you dont want this, leave blank): ")
                    if asz:
                        get_data(asz)
                else:
                    pass
        else:
            print("")
            list_1 = user_of_data.split(", ")
            dd = 0
            while dd < len(list_1):
                driver.get("https://www.instagram.com/" + list_1[dd] + "/")
                try:
                    driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                    print("User '" + list_1[dd] + "' not found :(")
                    print("")
                    dd += 1
                except NoSuchElementException:
                    a = []
                    b = []
                    all_spans = driver.find_elements_by_css_selector('.g47SY')
                    for span in all_spans:
                        b.append(span.get_attribute("title"))
                        a.append(span.text)
                    time.sleep(0.5)
                    if (b[1] == ""):
                        b[1] = a[1]
                    print(list_1[dd] + "'s data")
                    print("--------------------")
                    print(a[0] + " posts")
                    print(b[1] + " followers")
                    print(a[2] + " following")
                    print("--------------------")
                    print("")
                    dd += 1
            wwwap = input("Get another user(s) data? (y/n): ")
            if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                asz54 = input("Username to get data? (can be more than one separate by space and comma): ")
                if asz54:
                    get_data(asz54)
                else:
                    pass


    def get_photos():
        data_term = input("User to get photos links (empty if you dont want this): ")
        if (data_term == ""):
            sys.quit("Closed :)")
        driver.get("https://www.instagram.com/" + data_term + "/")
        time.sleep(0.5)
        print("")
        try:
            driver.find_element_by_css_selector(".QlxVY")
            print("User '" + data_term + "' have an private account!")
            print("")
            wwwa99 = input("Try other user? (y/n): ")
            if wwwa99 == "y" or wwwa99 == "Y" or wwwa99 == "yes" or wwwa99 == "Yes":
                get_photos()
            else:
                pass
        except NoSuchElementException:
            photos_links = []
            all_photos = driver.find_elements_by_css_selector('.FFVAD')
            for pht in all_photos:
                photos_links.append(pht.get_attribute("src"))
            i = 0
            while i < len(photos_links):
                print(photos_links[i])
                i += 1


    def get_id_user(user_to_get_id):
        if "," not in user_to_get_id:
            driver.get("https://www.instagram.com/" + user_to_get_id + "/?__a=1")
            print("")
            try:
                driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                print("User '" + user_to_get_id + "' not found :(")
                print("")
                wwwap = input("Try to get other user(s) ID's? (y/n): ")
                if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                    asz54 = input("Username to get ID? (can be more than one separate by space and comma): ")
                if asz54:
                    get_id_user(asz54)
                else:
                    pass
            except NoSuchElementException:
                contents = driver.find_element_by_tag_name("body")
                ddw = contents.text
                wqq = ddw[:ddw.find('",') + 1]
                wqq2 = wqq.replace('"logging_page_id":"profilePage_', '')
                x_fin = wqq2.replace('{', '')
                xs = x_fin.replace('"', '')
                print(user_to_get_id + "'s instagram ID: " + xs)
                print("")
                wwwap = input("Get another user(s) ID's? (y/n): ")
                if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                    asz54 = input("Username to get ID? (can be more than one separate by space and comma): ")
                    if asz54:
                        get_id_user(asz54)
                    else:
                        pass
        else:
            print("")
            list_1 = user_to_get_id.split(", ")
            dd = 0
            while dd < len(list_1):
                driver.get("https://www.instagram.com/" + list_1[dd] + "/?__a=1")
                try:
                    driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                    print("User '" + list_1[dd] + "' not found :(")
                    print("")
                    dd += 1
                except NoSuchElementException:
                    contents = driver.find_element_by_tag_name("body")
                    ddw = contents.text
                    wqq = ddw[:ddw.find('",') + 1]
                    wqq2 = wqq.replace('"logging_page_id":"profilePage_', '')
                    x_fin = wqq2.replace('{', '')
                    xs = x_fin.replace('"', '')
                    print(list_1[dd] + "'s instagram ID: " + xs)
                    print("")
                    dd += 1
            wwwap = input("Get another user(s) ID's? (y/n): ")
            if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                asz54 = input("Username to get ID? (can be more than one separate by space and comma): ")
                if asz54:
                    get_id_user(asz54)
                else:
                    pass
    def see_history():
        act1 = input("Username to see stories: ")
        driver.get("https://www.instagram.com/" + act1 + "/")
        print("")
        try:
            driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
            print("User '" + act1 + "' not found :(")
            print("")
            wwwap = input("Try to see stories again (y/n): ")
            if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                see_history()
            else:
                pass
        except NoSuchElementException:
            try:
                driver.find_element_by_css_selector("._4Kbb_._54f4m")
                print("Profile is private...")
                wwwap = input("Try to see stories again (y/n): ")
                if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                    see_history()
                else:
                    pass
            except NoSuchElementException:
                try:
                    driver.implicitly_wait(3)
                    driver.find_element_by_css_selector(".RR-M-.h5uC0").click()
                    print("Seeing the stories of: " + act1)
                    time.sleep(0.25)
                    active = True
                    try:
                        while active == True:
                            driver.find_element_by_css_selector(".ow3u_").click()
                            time.sleep(0.5)
                        active = False
                    except NoSuchElementException:
                        print("All stories of " + act1 + " seen.")
                except NoSuchElementException:
                    print("This user don't have stories today.")

        wwwap = input("See an story again? (y/n): ")
        if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
            see_history()
        else:
            pass
    def block_users(usr_bl):
        if "," not in usr_bl:
            driver.get("https://www.instagram.com/" + usr_bl + "/")
            print("")
            try:
                driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                print("User '" + usr_bl + "' not found :(")
                print("")
                wwwap = input("Try to block other user(s) (y/n): ")
                if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                    asz54 = input("Username to block ID? (can be more than one separate by space and comma): ")
                if asz54:
                    block_users(asz54)
                else:
                    pass
            except NoSuchElementException:
                driver.find_element_by_css_selector(".AFWDX").click()
                time.sleep(0.5)
                driver.find_elements_by_class_name("aOOlW.HoLwm")[1].click()
                driver.implicitly_wait(1)
                driver.find_element_by_css_selector(".aOOlW.bIiDR").click()
                print(usr_bl + " blocked")
                print("")
                wwwap = input("Block another user(s) (y/n): ")
                if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                    asz54 = input("Username to block? (can be more than one separate by space and comma): ")
                    if asz54:
                        block_users(asz54)
                    else:
                        pass
        else:
            print("")
            list_1 = usr_bl.split(", ")
            dd = 0
            while dd < len(list_1):
                driver.get("https://www.instagram.com/" + list_1[dd] + "/")
                try:
                    driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                    print("User '" + list_1[dd] + "' not found :(")
                    print("")
                    dd += 1
                except NoSuchElementException:
                    driver.find_element_by_css_selector(".AFWDX").click()
                    time.sleep(0.5)
                    driver.find_elements_by_class_name("aOOlW.HoLwm")[1].click()
                    driver.implicitly_wait(1)
                    driver.find_element_by_css_selector(".aOOlW.bIiDR").click()
                    print(list_1[dd] + " blocked")
                    print("")
                    dd += 1
            wwwap = input("Get another user(s) ID's? (y/n): ")
            if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                asz54 = input("Username to get ID? (can be more than one separate by space and comma): ")
                if asz54:
                    block_users(asz54)
                else:
                    pass
    def give_likes(usr_lik):
        if "," not in usr_lik:
            driver.get("https://www.instagram.com/" + usr_lik + "/")
            print("")
            try:
                driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                print("User '" + usr_lik + "' not found :(")
                print("")
                wwwap = input("Try to like other user(s) (y/n): ")
                if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                    asz54 = input("Username to like? (can be more than one separate by space and comma): ")
                if asz54:
                    give_likes(asz54)
                else:
                    pass
            except NoSuchElementException:
                try:
                    driver.find_element_by_css_selector("._4Kbb_._54f4m")
                    print(usr_lik + "'s profile is private...")
                    wwwap = input("Try to like other user(s) (y/n): ")
                    if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                        asz54 = input("Username to like? (can be more than one separate by space and comma): ")
                        if asz54:
                            give_likes(asz54)
                    else:
                        pass
                except NoSuchElementException:
                    try:
                        driver.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")[0].click() # Double click for select & enter
                        driver.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")[0].click()
                        time.sleep(0.5)
                        active = True
                        driver.implicitly_wait(2)
                        try:
                            while active == True:
                                driver.find_element_by_class_name("dCJp8.afkep.coreSpriteHeartOpen._0mzm-").click()
                                time.sleep(0.25)
                                driver.find_element_by_css_selector(".HBoOv.coreSpriteRightPaginationArrow").click()
                                time.sleep(0.4)
                            active = False
                        except NoSuchElementException:
                            print("All photos of " + usr_lik + " liked.")
                    except NoSuchElementException:
                        print("This user dont have photos!")
                print("")
                wwwap = input("Give like another user(s) (y/n): ")
                if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                    asz54 = input("Username to like? (can be more than one separate by space and comma): ")
                    if asz54:
                        give_likes(asz54)
                else:
                    pass
        else:
            print("")
            list_1 = usr_lik.split(", ")
            dd = 0
            while dd < len(list_1):
                driver.get("https://www.instagram.com/" + list_1[dd] + "/")
                try:
                    driver.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                    print("User '" + list_1[dd] + "' not found :(")
                    print("")
                    dd += 1
                except NoSuchElementException:
                    try:
                        driver.find_element_by_css_selector("._4Kbb_._54f4m")
                        print(list_1[dd] + "'s profile is private...")
                        print("")
                        dd += 1
                    except NoSuchElementException:
                        try:
                            driver.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")[0].click()  # Double click for select & enter
                            driver.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")[0].click()
                            time.sleep(0.5)
                            active = True
                            driver.implicitly_wait(2)
                            try:
                                while active == True:
                                    driver.find_element_by_class_name("dCJp8.afkep.coreSpriteHeartOpen._0mzm-").click()
                                    time.sleep(0.25)
                                    driver.find_element_by_css_selector(".HBoOv.coreSpriteRightPaginationArrow").click()
                                    time.sleep(0.4)
                                active = False
                            except NoSuchElementException:
                                print("All photos of " + list_1[dd] + " liked.")
                                dd += 1
                        except IndexError:
                            print(list_1[dd] + " dont have photos!")
                            dd += 1
                        print("")
            wwwap = input("Give like another user(s) (y/n): ")
            if wwwap == "y" or wwwap == "Y" or wwwap == "yes" or wwwap == "Yes":
                asz54 = input("Username to like? (can be more than one separate by space and comma): ")
                if asz54:
                    give_likes(asz54)
            else:
                pass

    if logged == "true":
        def main_act():
            print("")
            print("Select an option from the menu")
            print("==============================")
            print("""
            1) Grab user(s) data \n         
            2) Get Instagram ID \n
            3) Get photo links (only one user per input) \n
            4) See user stories (only one user per input) \n
            5) Block user \n
            6) Like photos of user(s) \n
            7) Logout""")
            option_num = int(input("Number?: "))
            if option_num == 1:
                user_of_data = input("Username to get data? (if you dont want this, leave blank): ")
                get_data(user_of_data)
                rpt = input("Want to use an tool again? (y/n): ")
                if rpt == "y" or rpt == "Y" or rpt == "yes" or rpt == "Yes":
                    main_act()
                else:
                    driver.quit()
                    sys.exit(0)
            elif option_num == 2:
                user_to_get_id = input("Username(s) to get Instagram ID: ")
                get_id_user(user_to_get_id)
                rpt = input("Want to use an tool again? (y/n): ")
                if rpt == "y" or rpt == "Y" or rpt == "yes" or rpt == "Yes":
                    main_act()
                else:
                    driver.quit()
                    sys.exit(0)
            elif option_num == 3:
                get_photos()
                rpt = input("Want to use an tool again? (y/n): ")
                if rpt == "y" or rpt == "Y" or rpt == "yes" or rpt == "Yes":
                    main_act()
                else:
                    driver.quit()
                    sys.exit(0)
            elif option_num == 4:
                see_history()
                rpt = input("Want to use an tool again? (y/n): ")
                if rpt == "y" or rpt == "Y" or rpt == "yes" or rpt == "Yes":
                    main_act()
                else:
                    driver.quit()
                    sys.exit(0)
            elif option_num == 5:
                usr_bl = input("Username to block?: ")
                block_users(usr_bl)
                rpt = input("Want to use an tool again? (y/n): ")
                if rpt == "y" or rpt == "Y" or rpt == "yes" or rpt == "Yes":
                    main_act()
                else:
                    driver.quit()
                    sys.exit(0)
            elif option_num == 6:
                usr_lik = input("Username to give like?: ")
                give_likes(usr_lik)
                rpt = input("Want to use an tool again? (y/n): ")
                if rpt == "y" or rpt == "Y" or rpt == "yes" or rpt == "Yes":
                    main_act()
                else:
                    driver.quit()
                    sys.exit(0)
            elif option_num == 7:
                print("Logout.")
                driver.quit()
                sys.exit(0)
        main_act()

    elif logged == "false":
        print("Not logged.")

elif sl == '2':
    print(''' \033[36m	<<<<< Instagram Grabber v''' + inst_g_v + ''' >>>>>
    You can grab many data of users \n
    usage : python3 instagram_grabber.py
    What's account.dat: file with login data in [username:password]
    Get Photos: grab photo links of an user
    Logout: close the browser.
    Block user: block the user.
    Like photos: this likes ALL user photos, but you can cancel it clicking out of the pop-up window on instagram
    Get data : get number of post, followers and following of the user.\033[0m''')
    sys.exit(0)
else:
    print("Incorrect Option.")
    sys.exit(1)
