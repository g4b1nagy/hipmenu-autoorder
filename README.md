# hipmenu-autoorder
Create group orders and post them to Skype automagically


### Getting your hands dirty ###

* cd to a comfy location
* git clone https://github.com/g4b1nagy/hipmenu-autoorder.git
* cd hipmenu-autoorder/
* virtualenv -p $(which python3) venv
* source venv/bin/activate
* pip install -r requirements.txt
* cp config_example.py config.py
* update the config.py file to suit your needs
* crontab -e
* 0 09 * * 1,2,3 /home/pi/hipmenu-autoorder/order.sh (run on Monday, Tuesday, Wednesday at 9 AM)
