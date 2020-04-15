counter = 1
while counter < 10:
    shutil.copyfile('/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/src/output/placeholder.jpg', f'/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/src/output/img{counter}.jpg')
    counter += 1