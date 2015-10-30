NIGHTLY64 = "C:/Program Files/Nightly/firefox.exe"
GENREL32 = "C:/Program Files (x86)/Mozilla Firefox/firefox.exe"


App.open(GENREL32)

click("1446153249015.png")

sleep(2)

if exists("1446153637218.png"):
    click("1446153637218.png") 

print "here?"

wait("1446153338359.png")

waitVanish("1446153338359.png")

print "yay"

click("1446154091312.png")

