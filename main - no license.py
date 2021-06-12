import random
import threading as thread
import tkinter as tk
import tkinter.messagebox as tm
from time import ctime, sleep, time
import selenium.common.exceptions
from RandomWordGenerator import RandomWord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib3.exceptions
random_word = RandomWord()
secret_word = random_word.generate()
account = -1

def die():
    global killed
    killed = 1
    tk.Label(window, text="\nWaiting until all precesses are done\n") \
        .grid(row=5, column=0, columnspan=4, padx=1, pady=1)
    for i in browser_list:
        i.join()


def openbrowser():
    rnd = 0
    global account, browser
    prox = random.choice(proxy_list)
    killed = 0
    blocked = 0
    while killed != 1:
        proxybutton = proxy_button.get()
        uname = username.get()
        passwd = password.get()
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--no-sandbox')
        if proxy_list != [] and proxybutton != 0:
            print('Using proxy: ',prox)
            chrome_options.add_argument('--proxy-server='+prox)

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
        wait = WebDriverWait(driver, 60)
        driver.set_window_size(350, 400)
        
        try:
            driver.get('https://aioz.tube/')
        except selenium.common.exceptions.WebDriverException:
            prox = random.choice(proxy_list)
            chrome_options.add_argument('--proxy-server=' + prox)
            try:
                driver.get('https://aioz.tube/')
            except selenium.common.exceptions.WebDriverException:
                print('Couldn\'t connect')
                driver.quit()
                open_multi()
                break

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/button')))
        except:
            driver.refresh()
        driver.find_element_by_xpath('/html/body/div[3]/div/div/div/button').click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   '#aioz-sidebar-content > div.aioz-sidebar-content > div > div.sticky > div > button.btn.btn-1')))
        driver.find_element_by_css_selector(
            '#aioz-sidebar-content > div.aioz-sidebar-content > div > div.sticky > div > button.btn.btn-1').click()

        wait.until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element_by_id('email').send_keys(uname)

        driver.find_element_by_id('password').send_keys(passwd)

        print('logging in with: ', uname)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.fade.modal.show > div > div > div > div > form > div.form-group.mt-4 > button')))
        driver.find_element_by_css_selector('body > div.fade.modal.show > div > div > div > div > form > div.form-group.mt-4 > button').click()
        try:
            wait.until(EC.invisibility_of_element_located((By.ID, 'password')))
        except selenium.common.exceptions.TimeoutException:
            try:
                if driver.find_element_by_class_name('error-msg').is_displayed():
                    print('Maybe blocked')
                    driver.quit()
                    browsers.delete(0, 'end')
                    browsers.insert(0, 1)
                    check.select()
                    driver.quit()

                    open_multi()
                    break
            except:
                driver.quit()
                browsers.delete(0, 'end')
                browsers.insert(0, 1)
                check.select()
                driver.quit()

                open_multi()
                break

        try:
            wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[3]/div/div/main/div[1]/div/div/div[2]/div/div[1]/a/div')))
            driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[3]/div/div/main/div[1]/div/div/div[2]/div/div[1]/a/div').click()
        except:
            driver.refresh()

        clicked = []
        while killed != 1:
            try:
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vjs-marker')))
                s = driver.find_elements_by_class_name('vjs-marker')

                for i in s:
                    if i not in clicked and killed != 1:
                        try:
                            wait = WebDriverWait(driver, 90)
                            sleep(random.choice(range(3, 5)))
                            i.click()
                            clicked.append(i)
                            # print('Opening ad number: ', clicked.index(i) + 1)
                            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'skip-ad-countdown')))
                            # print("skip-ad-countdown is running")
                            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'skip-ad-countdown')))
                            # print("skip-ad-countdown finished")
                            try:
                                wait = WebDriverWait(driver, 120)
                                wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'skip-ad')))
                            except selenium.common.exceptions.TimeoutException:
                                print('Time up, skipping the ad..')
                                driver.find_element_by_class_name('skip-ad').click()
                                continue

                            # print('skip-ad is out')
                            # print("finished waiting...")
                        except selenium.common.exceptions.TimeoutException:
                            print('Time out')
                            sleep(0.5)
                        except selenium.common.exceptions.ElementNotInteractableException:
                            sleep(0.5)
                clicked.clear()
                if rnd >= 5:
                    driver.quit()
                    print('finished round', rnd)
                    print(account, user)
                    check.select()
                    browsers.delete(0, 'end')
                    browsers.insert(0, 1)

                    open_multi()
                    break
                # print('Opening new vid...')

                driver.find_element_by_cpath('/html/body/div[1]/div/div[3]/div/div/main/div/div/div[2]/div/div/div[1]/div[1]/a/div').click()

                blocked = 0
                rnd += 1

            except selenium.common.exceptions.ElementClickInterceptedException:
                sleep(0.5)
            except selenium.common.exceptions.TimeoutException:
                driver.refresh()

                blocked += 1
                print('refreishing', blocked)
                if blocked >= 3:
                    print(f'Blocked is:{blocked} and openeing new browser')
                    driver.quit()
                    print(account, user)
                    browsers.delete(0 ,'end')
                    browsers.insert(0, 1)
                    #open_multi()
                    break

            except urllib3.exceptions.MaxRetryError or urllib3.exceptions.NewConnectionError or ConnectionRefusedError:
                sleep(0.5)
                continue



def open_multi():
    global browser_list, killed, user, pas, proxy_list, account
    with open('accounts.txt') as acc:
        acc = acc.read().split('\n')
        user = acc[::2]
        pas = acc[1::2]
        username.delete(0, "end")
        password.delete(0, 'end')
        account += 1
        if account >= len(user):
            account = 0
        username.insert(0, user[account])
        password.insert(0, pas[account])

    browser = browsers.get()
    with open('proxy.txt') as pr:
        proxy_list = pr.read().split('\n')

    killed = 0
    browser_list = []
    for i in range(int(browser)):
        browser_list.append(thread.Thread(target=openbrowser))
        print(browser_list, browser)
        browser_list[i].start()


def run_task():
    global browsers, username, password, browser, proxy_button, check

    tk.Label(window, text="Hi") \
        .grid(row=0, column=0, columnspan=4, padx=1, pady=1)

    tk.Label(window, text="How many Browsers do you want to open? ", justify='left') \
        .grid(row=1, column=0, padx=1, pady=1)

    browsers = tk.Entry(window, width=30)
    browsers.insert(0, "Put your desired number here")
    browsers.grid(row=1, column=2, padx=10)
    browsers.bind("<Button-1>", lambda event: browsers.delete(0, "end"))

    tk.Label(window, text="Enter your username: ", justify="left").grid(row=2, column=0)
    username = tk.Entry(window, width=30)
    username.insert(0, "put your username here")
    username.grid(row=2, column=2, padx=10)
    username.bind("<Button-1>", lambda event: username.delete(0, "end"))

    tk.Label(window, text="Enter your password: ", justify="left").grid(row=3, column=0)
    password = tk.Entry(window, width=30, show="*")
    password.insert(0, "Put your password here")
    password.grid(row=3, column=2, padx=10)
    password.bind("<Button-1>", lambda event: password.delete(0, "end"))

    proxy_button = tk.IntVar()
    check = tk.Checkbutton(window, text='Use Proxy', variable=proxy_button)
    check.grid(row=4, column=0)
    tk.Button(window, text="Start", command=open_multi, width=15, height=2). \
        grid(row=5, column=0, padx=1, pady=1)

    tk.Button(window, text="Stop", command=die, width=15, height=2). \
        grid(row=5, column=1, padx=1, pady=1)
    tk.Button(window, text="Quit", command=window.quit, width=15, height=2). \
        grid(row=5, column=2, padx=1, pady=1)
    conf = tk.Grid
    for i in range(5):
        conf.columnconfigure(window, i, weight=1)
        conf.rowconfigure(window, i, weight=1)
    tk.mainloop()


def main():
    global window, account
    window = tk.Tk()
    window.title("AIOZbot.exe")

 
    run_task()



if __name__ == '__main__':
    main()
