NIGHTLY64 = "C:/Program Files/Nightly/firefox.exe -height 768 -width 1024"
PATH_FIREFOX = NIGHTLY64
URL_TEST_PAGE = 'https://pdehaan.github.io/push-notification-test'

firefox = App('Nightly')
firefox.open(PATH_FIREFOX)
sleep(2)
firefox.focus()

click("1446160870518.png")

click("1446159886063.png")

type(URL_TEST_PAGE + Key.ENTER)

click("1446153249015.png")

sleep(2)

if exists("1446159501996.png"):
    click("1446159501996.png")

print "pop notification: here?"

wait("1446161475675.png")

print('pop notificaiton: waiting for vanish')

waitVanish("1446161475675.png")

print "DONE! --> close browser now"

firefox.close()


