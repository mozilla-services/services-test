NIGHTLY64 = "C:/Program Files/Nightly/firefox.exe -height 768 -width 1024"
PATH_FIREFOX = NIGHTLY64
APP_NAME = 'Nightly'
URL_TEST_PAGE = 'https://pdehaan.github.io/push-notification-test'

URL_ENTRY_POINT_1 = Pattern("1446175705142.png").targetOffset(110,-4)
URL_ENTRY_POINT_2 = "1446176591082.png"
URL_ENTRY_POINT_3 = Pattern("1446175756881.png").targetOffset(59,0)
URL_ENTRY_POINT_4 = Pattern("1446178093719.png").targetOffset(35,1)


def teardown():
    print('closing browser now')
    firefox.close()
    print('Firefox closed')

def setup():
    firefox = App(APP_NAME)
    firefox.open(PATH_FIREFOX)
    sleep(2)
    firefox.focus()

setup()

click("1446160870518.png")

if exists(URL_ENTRY_POINT_1):
    print('URL entry point: <Mozilla Foundation>')
    click(URL_ENTRY_POINT_1)
elif(URL_ENTRY_POINT_2):
    print('URL entry point: <Search or enter address>')
    click(URL_ENTRY_POINT_2)
elif(URL_ENTRY_POINT_3):
    print('URL entry point: <Nightly...>')
    click(URL_ENTRY_POINT_3)
else:
    print('URL entry point: <green padlock>')
    click(URL_ENTRY_POINT_4)
type(URL_TEST_PAGE + Key.ENTER)

click("1446153249015.png")

sleep(2)

print('<Always Receive Notifications?>')
if exists("1446176332222.png"):
    click("1446176332222.png")

print "pop notification: ???"

wait("1446161475675.png")
print('pop notification complete!')

print('pop notification: waiting for vanish')

waitVanish("1446161475675.png")

print('TEST COMPLETE!')

teardown()


