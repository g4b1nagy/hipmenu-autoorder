# hipmenu-autoorder

Create group orders and post them to Skype automagically


### What's this? ###

hipmenu-autoorder is a Selenium script that is used to automate the process of creating hipMenu group orders.


### How does it work? ###

The script opens up an instance of Firefox and then it:

* logs into Facebook
* logs into hipMenu, using the above Facebook account
* creates a new group order URL
* logs into Skype
* posts the group order URL to the relevant Skype discussion
* waits until 10:55 AM
* sends the group order to the restaurant
* and also sends some SMS alerts along the way


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
