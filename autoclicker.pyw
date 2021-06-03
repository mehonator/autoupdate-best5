import pyautogui
import time
import PIL

timeAfterStart = 10
timeBetweenMove = 3
pathPic = ""


def findClick(namePic, chekPic='', boxSearch=[0, 0, 1920, 1080]):
    if chekPic != "":
        boxSearch = pyautogui.locateOnScreen(pathPic + chekPic)

    x, y = pyautogui.locateCenterOnScreen((pathPic + namePic), region=boxSearch)
    print(x, y)
    pyautogui.moveTo(x, y, duration=timeBetweenMove, tween=pyautogui.easeInOutQuad)
    pyautogui.click()


try:

    print("start autoclicker for update")

    time.sleep(timeAfterStart)
    findClick("01вход_ок.png", chekPic="00вход.png")
    print("01вход_ок.png")
    time.sleep(timeBetweenMove)

    findClick("03вход_аптека_сиемма.png", chekPic="02вход_выбор_пред.png")
    print("03вход_аптека_сиемма.png")
    time.sleep(timeBetweenMove)

    # без проверки тк проверили в прошлый раз
    findClick("03вход_аптека_сиемма_ок.png")
    print("03вход_аптека_сиемма_ок.png")
    time.sleep(timeBetweenMove)

    # нет чек пикчи, тк октружение сильно меняется
    try:
        findClick("04главное меню_ненаж.png")
        print("04главное меню_ненаж.png")
    except TypeError:
        findClick("04главное меню_наж.png")
        print("04главное меню_наж.png")

    time.sleep(timeBetweenMove)

    findClick("05отрас_реш.png", chekPic="05отрас_реш.png")
    print("05отрас_реш.png")
    time.sleep(timeBetweenMove)

    findClick("06отрас_реш_апт2.png", chekPic="06отрас_реш_апт.png")
    print("06отрас_реш_апт2.png")
    time.sleep(timeBetweenMove)

    # нет чек пикчи, тк октружение сильно меняется
    findClick("07электронный приход.png")
    print("07электронный приход.png")
    time.sleep(timeBetweenMove)

    findClick("08выполнить.png", "08внимание_восстановление.png")
    print("08выполнить.png")
    time.sleep(timeBetweenMove)

except BaseException:
    print("ну, что-то пошло не так")
    input("введите что-нибудб чтобы закрыть")
