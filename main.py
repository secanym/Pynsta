from selenium import webdriver
from time import sleep
from login import meno1, heslo1
import datetime
import json

date_format = '%Y-%m-%d %H:%M:%S'


class Bot:
    following = []
    username = ''

    def __init__(self, username, password):
        self.username = username
        try:
            with open(self.username+'.txt', 'r') as filehandle:
                self.following = json.load(filehandle)
            print(self.following)
        except:
            print("Following database failed to load")
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.login(username, password)

    def login(self, username, password):
        self.driver.get("https://instagram.com")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Prijať')]") \
            .click()
        sleep(1)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]") \
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]") \
            .send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]') \
            .click()
        sleep(3)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Teraz nie')]") \
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Teraz nie')]") \
            .click()

    def shutdown(self):
        with open(self.username+'.txt', 'w') as filehandle:
            json.dump(self.following, filehandle)
        self.driver.quit()

    def follow(self, username):
        self.driver.get("https://instagram.com/" + username)
        sleep(2)
        try:
            self.driver.find_element_by_xpath('//button[@class ="_5f5mN       jIbKX  _6VtSN     yZn4P   "]') \
                .click()
        except:
            pass

        try:
            self.driver.find_element_by_xpath('//button[@class ="sqdOP  L3NKy   y3zKF     "]') \
                .click()
        except:
            pass

        time = datetime.datetime.now().strftime(date_format)
        self.following.append((username, time))
        sleep(1)

    def unfollow(self, username):
        self.driver.get("https://instagram.com/" + username)
        sleep(1)
        # Unfollow public account
        try:
            self.driver.find_element_by_xpath('//button[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]') \
                .click()
            self.driver.find_element_by_xpath('//button[@class="aOOlW -Cab_   "]') \
                .click()
        except:
            pass

        # Unfollow private account
        try:
            self.driver.find_element_by_xpath('//button[@class="sqdOP  L3NKy    _8A5w5    "]') \
                .click()
            self.driver.find_element_by_xpath('//button[@class="aOOlW -Cab_   "]') \
                .click()
        except:
            pass

        sleep(1)

        # Remove account from database
        for i in range(len(self.following)):
            if self.following[i][0] == username:
                self.following.pop(i)
                break

    def follow_list(self, list):
        for i in range(len(list)):
            self.follow(list[i])

    def autounfollow(self, hours):
        i = 0
        while True:
            if i == len(self.following):
                break
            time = datetime.datetime.now().strftime(date_format)
            time_diff = datetime.datetime.strptime(time, date_format) - datetime.datetime.strptime(self.following[i][1],
                                                                                                   date_format)
            if (time_diff.total_seconds() > hours * 3600):
                self.unfollow(self.following[i][0])
            else:
                i += 1

    def get_names_from_first_post(self, username, amount):
        self.driver.get("https://instagram.com/" + username)
        sleep(2)
        self.driver.find_element_by_class_name("kIKUG").click()
        sleep(3)
        self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button') \
            .click()
        sleep(5)

        scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div")

        names = []
        counter, last_ht, ht = 0, 0, 1
        while (last_ht != ht and counter < amount):
            last_ht = ht
            counter = len(names)
            sleep(1)
            ht = self.driver.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                        return arguments[0].scrollHeight;
                        """, scroll_box)
            sleep(1)
            links = scroll_box.find_elements_by_tag_name('a')
            temp = [name.text for name in links if name.text != '']
            for i in range(len(temp)):
                if temp[i] not in names:
                    names.append(temp[i])

        print(names)
        print(len(names))

        return names

    def clear_database(self):
        print('Following action will only clear database. It will NOT unfollow any user.')
        temp = input("Enter 'clear' to clear the database, enter anything else to skip.")

        if temp == 'clear':
            self.following = []
        else:
            pass

    def like_hashtag(self, hashtag, amount):
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag)
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]').click()
        for i in range(amount):
            sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
            if i == amount - 1:
                break
            sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()

def menu():
    Pysta = Bot(meno1, heslo1)

    while(True):
        print("1 - Follow username")
        print("2 - Unfollow username")
        print("3 - Follow 'likers' from first photo from account")
        print("4 - Unfollow accounts followed for certain time")
        print("5 - Like photos with certain hashtag")
        print("6 - Clear database")
        x = input("Enter number to choose, or type 'end' to close app: ")
        print("--------------------------------------------------------")
        if x == '1':
            username = input("Follow account: ")
            Pysta.follow(username)
        elif x == '2':
            username = input("Follow account: ")
            Pysta.unfollow(username)
        elif x == '3':
            username = input("First photo from accout: ")
            amount = int(input("Number of accouts to be followed: "))
            names = Pysta.get_names_from_first_post(username, amount)
            Pysta.follow_list(names[:amount])
        elif x == '4':
            hours = input("Unfollow accounts followed for more than(hours): ")
            Pysta.autounfollow(hours)
        elif x == '5':
            hashtag = input("Hashtag to like photos: ")
            amount = int(input("Number of photos to be liked: "))
            Pysta.like_hashtag(hashtag, amount)
        elif x == '6':
            Pysta.clear_database()
        elif x == '7':
            pass
        elif x == 'end':
            Pysta.shutdown()
            return 0
        print("--------------------------------------------------------")


if __name__ == '__main__':
    # menu()
    input("Press ENTER to run bot")

    arnost = Bot(meno1, heslo1)
    arnost.like_hashtag('nature',5)

    x = input('Press ENTER to shutdown')
    arnost.shutdown()

# EXPORT
# with open('listfile.txt', 'w') as filehandle:
#     json.dump(follownames, filehandle)
#
# IMPORT
# with open('listfile.txt', 'r') as filehandle:
#     zoznaaam = json.load(filehandle)
