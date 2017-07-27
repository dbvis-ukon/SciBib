chmod +x bin/cake
bin/cake migrations migrate -p CakeDC/Users
bin/cake users addSuperuser
