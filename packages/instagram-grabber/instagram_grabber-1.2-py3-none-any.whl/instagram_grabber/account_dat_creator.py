def cr_mod_account(username11, pass22):
    global i
    i = 0
    try:
        file_c = open('account.dat')
        file_c.close()
        i = 1
    except FileNotFoundError:
        i = 2
    else:
        pass
    if i == 1:
        file_c = open('account.dat', 'w+')
        file_c.write(username11 + ":" + pass22)
        file_c.close()
        print("Login file modified.")
    elif i == 2:
        file_c = open('account.dat', 'w+')
        file_c.write(username11 + ":" + pass22)
        file_c.close()
        print("Login file created!")
    else:
        print("Error.")
