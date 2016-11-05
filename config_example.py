CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'

FACEBOOK = {
    'email': '',
    'password': '',
}

HIPMENU = {
    'restaurant_url': 'https://www.hipmenu.ro/#p1/rg/cluj-prod/group/98254//',
}

SKYPE = {
    'username': '',
    'password': '',
    'conversation_title': '',
}

NEXMO = {
    'api_key': '',
    'api_secret': '',
    'phone_number': '40744444444',
}

ORDERS_SCRIPT = """
var orders = [];
var order_tags = document.querySelectorAll('.history-diners .container-marginTBMedium');
for (var i = 0; i < order_tags.length; i++) {
    var tds = order_tags[i].querySelectorAll('footer td');
    orders.push({
        name: order_tags[i].querySelector('h4').textContent.trim(),
        price: tds[tds.length - 1].textContent.trim(),
    });
}
return orders;
"""

TEST = True
