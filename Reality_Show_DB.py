import mysql.connector
mydb = mysql.connector.connect(host='localhost',user='root',password='krupa123',database='reality_show')
mycursor = mydb.cursor()

class user_details:
    def __init__(self, user_name, password, role_no):
        self.user_name = user_name
        self.password = password
        self.role_no = role_no

    def validate(self):
        mycursor.execute('select user_id,user_name,password from user_details where user_name like %s '
                         'and role_id like %s',(self.user_name, self.role_no,))
        details = mycursor.fetchall()
        if (len(details) != 0):
            if(self.user_name == details[0][1] and self.password == details[0][2]):
                return details[0][0]

class language:
    def selectLang(self):
        mycursor.execute('select * from language')
        datailsLang = mycursor.fetchall()
        print('------------------------------------------------------')
        print('LIST OF LANGUAGES:-')
        for i in datailsLang:
            print('        ',str(i[0])+'.',i[1])
        chooseLang = input('Select your preferred Language_no: ')
        return chooseLang

class channel_details():
    def __init__(self,lang_id):
        self.lang_id = lang_id

    def selectChannel(self):
        mycursor.execute('select channel_id,channel_name,channel_rating,channel_ceo from channel_details where'
                         ' lang_id like %s',(self.lang_id,))
        detailsChannel = mycursor.fetchall()
        num = 1
        print('------------------------------------------------------')
        print('LIST OF CHANNELS:-')
        for i in detailsChannel:
            print('        ',str(num)+'. '+i[1],'     rating:',i[2],'   CEO:',i[3])
            num+=1
        chooseChannel = input('Select your preferred Channel_no: ')
        return chooseChannel

class reality_show_details():
    def __init__(self,channel_id):
        self.channel_id = channel_id

    def selectShow(self):
        mycursor.execute('select * from reality_show_details where channel_id like %s',(self.channel_id,))
        detailsShow = mycursor.fetchall()
        print('------------------------------------------------------')
        print('LIST OF REALITY SHOWS:-')
        for i in detailsShow:
            print('        ',str(i[0])+'.',i[2],'    rating:',i[3],'    Host:',i[4])
        chooseShow = input('Select your preferred Show_no: ')
        return chooseShow

class contestants_details():
    def __init__(self,show_id):
        self.show_id = show_id

    def selectCont(self):
        mycursor.execute('select cont_id,cont_name,cont_age,judges_rating,votes_received from contestants_details '
                         'where show_id like %s',(self.show_id,))
        detailsCont = mycursor.fetchall()
        print('------------------------------------------------------')
        print('LIST OF CONTESTANTS:-')
        for i in detailsCont:
            print('        ',str(i[0])+'.',i[1],'     Age:',i[2],'     Judges_rating:',i[3],'     Votes_received:',i[4])
        print()
        choice = input('Do you want to see insights of weekly and daily ratings of contestants Yes/No: ')
        if(choice=='Yes'):
            favo = input('Select your wished contestant_no: ')
            Choice = input('Choose your preferrence (weekly: 1/daily: 2): ')
            if(Choice=='1'):
                from_date = input('Enter From date (dd/mm/yyyy): ')
                To_date = input('Enter To date (dd/mm/yyyy): ')
                mycursor.execute('select performance_date,perfromance_rating from performance_record where performance_date'
                                 ' between %s and %s and cont_id like %s',(from_date,To_date,favo,))
                detailsweek = mycursor.fetchall()
                print('------------------------------------------------------')
                print('LIST OF WEEKLY PERFORMANCE RATINGS OF CHOOSEN CONTESTANTS:-')
                print(' '*10,'performance_date:',' '*12,'perfromance_rating:')
                for i in detailsweek:
                    print(' '*13,i[0],'                ',i[1])

            else:
                selectDate = input('Enter preferred date (dd/mm/yyyy): ')
                mycursor.execute('select performance_date,perfromance_rating from performance_record where performance_date'
                                 ' like %s and cont_id like %s',(selectDate,favo,))
                detailsDaily = mycursor.fetchall()
                print('\nCHOOSEN CONTESTANT RATING ON',selectDate,': ',detailsDaily[0][1])

class eliminated_cont:
    def __init__(self, show_id):
        self.show_id = show_id

    def EliminatedCont(self):
        mycursor.execute('select cont_id,cont_name,cont_age,votes_received from contestants_details '
                         'where show_id like %s and votes_received<=3500',(self.show_id,))
        detailsEliminate = mycursor.fetchall()
        print('------------------------------------------------------')
        print('LIST OF ELIMINATED CONTESTANTS WHO RECEIVED VOTES<=3500:-')
        for i in detailsEliminate:
            print(' '*8,i[0],'.',' '*6,i[1],' '*6,'Age:',i[2],' '*6,'Votes_received:',i[3])
        choose_favo = input('Select Contestant_no You want to Vote from the above list: ')
        print('------------------------------------------------------')
        print(' '*8,'TIME TO VOTE YOUR FAVOURITE CONTESTANT!!!')
        poll_vote = input('Give your votes (maxi 100 votes): ')
        mycursor.execute('select cont_name from contestants_details where cont_id like %s', (choose_favo,))
        cont_name = mycursor.fetchall()
        print('\n----------------Your votes for',cont_name[0][0].upper(),'is polled successfully!!!----------------')



if __name__ == '__main__':
    role_no = input('\nEnter your role_no (admin: 1/user: 2): ')
    user_name = input('Enter your name: ')
    password = input('Enter your password: ')

    displayUserDetails = user_details(user_name, password, role_no)
    Validate = displayUserDetails.validate()

    if(Validate):
        displayLang = language()
        lang_id = displayLang.selectLang()

        displaychannel = channel_details(lang_id)
        channel_id = displaychannel.selectChannel()

        displayshow = reality_show_details(channel_id)
        show_id = displayshow.selectShow()

        displayCont = contestants_details(show_id)
        displayCont.selectCont()

        displayEliminatedCont = eliminated_cont(show_id)
        displayEliminatedCont.EliminatedCont()

    else:
        phone_no = input('Enter your phone_no: ')
        email_id = input('Enter your email_id: ')
        mycursor.execute('insert into user_details(role_id,user_name,email_id,password,phone_no) '
                         'values(%s,%s,%s,%s,%s)',(role_no,user_name,email_id,password,phone_no,))
        mydb.commit()
