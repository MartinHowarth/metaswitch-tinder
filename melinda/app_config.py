"""The configuration for the app."""

from melinda.config_model import Melinda

raw_config = {
    "app_name": "Melinda",
    "ducks": [
        "https://images-na.ssl-images-amazon.com/images/I/51Hv7fTTaLL._SX425_.jpg",
        "https://i.pinimg.com/originals/8b/e8/41/8be841dbba8e6c633728ffe1580a930f.jpg",
    ],
    "serious_ducks": [
        "https://images-na.ssl-images-amazon.com/images/I/31g29UpRHQL._SX450_.jpg",
        "https://images-na.ssl-images-amazon.com/images/I/31p4yBHv7OL.jpg",
        "https://images-na.ssl-images-amazon.com/images/I/610WVKNC0OL._SL1024_.jpg",
    ],
    "sad_ducks": [
        "https://vignette.wikia.nocookie.net/uncyclopedia/images/6/60/"
        "Sad_duck.jpg/revision/latest?cb=20090621212341"
    ],
    "default_user_image": "https://is2-ssl.mzstatic.com/image/thumb/Purple71/"
    "v4/c9/f9/d1/c9f9d1e4-b9f1-6bf2-5846-199528ddab8e/source/512x512bb.jpg",
    "report_email_address": "howarth.martin@gmail.com",
}

config = Melinda(raw_config, partial=False)
config.validate()

if __name__ == "__main__":
    import json

    print(json.dumps(config))
