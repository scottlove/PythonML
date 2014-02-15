# This code is supporting material for the book
# Building Machine Learning Systems with Python
# by Willi Richert and Luis Pedro Coelho
# published by PACKT Publishing
#
# It is made available under the MIT License


import sys


CONSUMER_KEY = "WZZdn9mMTfObL050c6XqzQ"
CONSUMER_SECRET = "vqFmWXGn10zLHQZjGkUkM3G3rHawBq3UCg7pumwaM"


ACCESS_TOKEN_KEY = "2342509315-yUmI78g8VVwN6XUwY2lc1QWc5FHdI2bLqADruaH"
ACCESS_TOKEN_SECRET = "9273D7hn7vtQk6lLJgaJtOdCibqKEQAFIzNeUXTkfKY5T"


if CONSUMER_KEY is None or CONSUMER_SECRET is None or ACCESS_TOKEN_KEY is None or ACCESS_TOKEN_SECRET is None:
    print("""\
When doing last code sanity checks for the book, Twitter
was using the API 1.0, which did not require authentication.
With its switch to version 1.1, this has now changed.


It seems that you don't have already created your personal Twitter
access keys and tokens. Please do so at
https://dev.twitter.com/docs/auth/tokens-devtwittercom
and paste the keys/secrets into twitterauth.py


Sorry for the inconvenience,
The authors.""")


    sys.exit(1)


