import gspread

gc = gspread.service_account(filename='')

sheet = gc.open('NewsProject')

worksheet = sheet.worksheet('Users')



def getusers():
    users = worksheet.col_values(1)
    return users[1:]

def is_User(id):
    users = worksheet.col_values(1)
    for i in range(1,len(users)):
        if int(users[i]) == int(id):
            return True
    False



def finduser(id):
    users = worksheet.col_values(1)
    index = 1
    for i in range(1,len(users)):
        if int(users[i]) == id:
            index += i
    return index

def adduser(newUser):
    users = worksheet.col_values(1)
    new_user_position = len(users) + 1
    cell_address = F'A{new_user_position}'
    update = [{'range': cell_address, 'values': [[newUser]]}]
    worksheet.batch_update(update)


def deleteuser(chatid):
    user = finduser(chatid)
    worksheet.delete_row(user)


