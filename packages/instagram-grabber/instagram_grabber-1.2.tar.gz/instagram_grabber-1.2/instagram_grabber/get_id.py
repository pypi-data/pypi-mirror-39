from insta import webdriver

dr2 = webdriver.Firefox()


def get_id_user(user_to_get_id):
    if "," not in user_to_get_id:
        dr2.get("https://www.instagram.com/" + user_to_get_id + "/?__a=1")
        print("")
        try:
            dr2.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
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
            contents = dr2.find_element_by_tag_name("body")
            ddw = contents.text
            for line in ddw.splitlines():
                if "logging_page_id" in line:
                    aa = line
                    azw = aa.replace('logging_page_id "profilePage_', '')
            print("")
    else:
        print("")
        list_1 = user_to_get_id.split(", ")
        dd = 0
        while dd < len(list_1):
            dr2.get("https://www.instagram.com/" + list_1[dd] + "/?__a=1")
            try:
                dr2.find_element_by_css_selector(".main.-cx-PRIVATE-Page__main.-cx-PRIVATE-Page__main__")
                print("User '" + list_1[dd] + "' not found :(")
                print("")
                dd += 1
            except NoSuchElementException:
                contents = dr2.find_element_by_tag_name("body")
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