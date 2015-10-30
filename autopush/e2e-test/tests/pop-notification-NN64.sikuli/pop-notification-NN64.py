NIGHTLY64 = "C:/Program Files/Nightly/firefox.exe -height 768 -width 1024"
PATH_FIREFOX = NIGHTLY64
PATH_IMGS = '../images/'
APP_NAME = 'Nightly'
URL_TEST_PAGE = 'https://pdehaan.github.io/push-notification-test'

IMG_REFRESH_NIGHTLY = PATH_IMGS + "1446181480598.png"  
# moz foundation
URL_ENTRY_POINT_1 = Pattern(PATH_IMGS + "1446175705142.png").targetOffset(110,-4)
#search
URL_ENTRY_POINT_2 = PATH_IMGS + "1446176591082.png"
# nightly
URL_ENTRY_POINT_3 = Pattern(PATH_IMGS + "1446175756881.png").targetOffset(59,0)
# green padlock
URL_ENTRY_POINT_4 = Pattern(PATH_IMGS + "1446178093719.png").targetOffset(35,1)

IMG_WIN_MAXIMIZE = PATH_IMGS + "1446160870518.png"
IMG_ALWAYS_RECEIVE_NOTIFICATIONS = PATH_IMGS + "1446176332222.png"
IMG_BTN_POP_NOTIFICATION = PATH_IMGS + "1446153249015.png"
IMG_WIN_POP_NOTIFICATION = PATH_IMGS + "1446161475675.png"
LINE = '--------------------------'



def setup():
    
    print('%s\n%s\n%s' % (LINE, 'SETUP', LINE))
    firefox = App(APP_NAME)
    firefox.open(PATH_FIREFOX)
    if exists(IMG_REFRESH_NIGHTLY):
        click(IMG_REFRESH_NIGHTLY)
        click(IMG_REFRESH_NIGHTLY)
    firefox.focus()

def teardown():

    print('%s\n%s\n%s' % (LINE, 'TEARDOWN', LINE))
    print('closing browser now')
    firefox.close()
    print('Firefox closed')
    
setup()

if exists(URL_ENTRY_POINT_1):
    print('URL ENTRY POINT: <Mozilla Foundation>')
    click(URL_ENTRY_POINT_1)
elif(URL_ENTRY_POINT_2):
    print('URL ENTRY POINT: <Search or enter address>')
    click(URL_ENTRY_POINT_2)
elif(URL_ENTRY_POINT_3):
    print('URL ENTRY POINT: <Nightly...>')
    click(URL_ENTRY_POINT_3)
else:
    print('URL ENTRY POINT: <green padlock>')
    click(URL_ENTRY_POINT_4)
type(URL_TEST_PAGE + Key.ENTER)

click(IMG_BTN_POP_NOTIFICATION)

sleep(2)

print('PERMISSIONS: <Always Receive Notifications?>')
if exists(IMG_ALWAYS_RECEIVE_NOTIFICATIONS):
    click(IMG_ALWAYS_RECEIVE_NOTIFICATIONS)

print "POP NOTIFICATION: ???"
wait(IMG_WIN_POP_NOTIFICATION)
print('POP NOTIFICATION: COMPLETE!')
print('POP NOTIFICATION: WAITING FOR VANISH.....')
waitVanish(IMG_WIN_POP_NOTIFICATION)
print('TEST COMPLETE!')

teardown()


