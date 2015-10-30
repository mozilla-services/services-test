APP_NAME = 'Nightly'
#APP_NAME = 'Release'
NIGHTLY64 = "C:/Program Files/%s/firefox.exe -height 768 -width 1024" % APP_NAME
PATH_FIREFOX = NIGHTLY64

if APP_NAME == 'Nightly':
    PATH_IMGS = '../images_nightly64/'
else:
    PATH_IMGS = '../images_release32/'
    print('TBD -> need images for GR32!!')
    exit(1) 
    

URL_TEST_PAGE = 'https://pdehaan.github.io/push-notification-test'

IMG_REFRESH = PATH_IMGS + "btn_refresh.png" # 
URL_ENTRY_POINT_1 = Pattern(PATH_IMGS + "url_entry_moz.png").targetOffset(110,-4)
URL_ENTRY_POINT_2 = PATH_IMGS + "url_entry_search.png" 
URL_ENTRY_POINT_3 = Pattern(PATH_IMGS + "url_entry_nightly.png").targetOffset(59,0)
URL_ENTRY_POINT_4 = Pattern(PATH_IMGS + "url_entry_green_padlock.png").targetOffset(59,1)
IMG_WIN_MAXIMIZE = PATH_IMGS + "win_maximize.png" 
IMG_ALWAYS_RECEIVE_NOTIFICATIONS = PATH_IMGS + "btn_always_receive.png"
IMG_BTN_POP_NOTIFICATION = PATH_IMGS + "btn_pop_notification.png" 
IMG_WIN_POP_NOTIFICATION = PATH_IMGS + "win_pop_notification.png" 
LINE = '--------------------------'


firefox = App(APP_NAME)

def header(label):
    return '%s\n%s\n%s' % (LINE, label, LINE)
    
def setup():
    
    print header('SETUP')
    firefox.open(PATH_FIREFOX)
    if exists(IMG_REFRESH):
        click(IMG_REFRESH)
        click(IMG_REFRESH)
    firefox.focus()

def teardown():

    #print('%s\n%s\n%s' % (LINE, 'TEARDOWN', LINE))
    print header('TEARDOWN')
    print('closing browser now')
    firefox.close()
    print('Firefox closed')
    
setup()

print header('TEST')

if exists(URL_ENTRY_POINT_1):
    print('URL ENTRY POINT: <Mozilla Foundation>')
    click(URL_ENTRY_POINT_1)
elif exists(URL_ENTRY_POINT_2):
    print('URL ENTRY POINT: <Search or enter address>')
    click(URL_ENTRY_POINT_2)
elif exists(URL_ENTRY_POINT_3):
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