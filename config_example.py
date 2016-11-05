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

TEST = True

orders_script = """
var orders = [];
var my_name = document.querySelector('#h-profilename').textContent;
var name_tags = Array.prototype.slice.call(document.querySelectorAll('.container-white-rounded .header-left p'));
var price_tags = Array.prototype.slice.call(document.querySelectorAll('.container-white-rounded .summary-total .value'));
if (name_tags.length > price_tags.length) {
    name_tags.splice(0, 1);
}
for (var i = 0; i < name_tags.length; i++) {
    orders.push({
        name: name_tags[i].textContent.replace('Selecțiile mele', my_name).trim(),
        price: price_tags[i].textContent.trim(),
    });
}
return orders;
"""
