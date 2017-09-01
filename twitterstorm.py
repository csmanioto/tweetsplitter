import tweepy
import time,  sys


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

autorizar = tweepy.OAuthHandler(consumer_key, consumer_secret)
autorizar.set_access_token(access_token, access_token_secret)
api = tweepy.API(autorizar)
api_config = api.configuration()


def splitter(data, limit_char):
    bag_word = data.split()
    output_list = []
    phrase = ''
    chunk = 1

    if len(data) <= limit_char:
        output_list.append(data)
        return output_list

    phrase = 'Chunk {}/@@ '.format(chunk)

    for idx in range(len(bag_word)):
        word = bag_word[idx] + ' '

        # The URL will be shorted by tweepy. No matter how long is the url, all will be fixed by short_url_length
        if "http" in word:
            lenp = len(phrase) + api_config['short_url_length']
        else:
            lenp = len(phrase) + len(word)

        if lenp > limit_char:
            chunk += 1
            output_list.append(phrase)
            phrase = 'Chunk {}/@@: '.format(chunk)
        else:
            phrase += word

    # Take the rest of phrase and put in the list.
    if len(phrase) > 0:
        phrase += word
        output_list.append(phrase)

    return output_list


def tweeting(tweets, rate_limit):
    try:
        total_message = len(tweets)

        for tweet in reversed(tweets):
            text  = tweet.replace('@@', str(total_message))
            api.update_status(status=text)
            print("Tweeting message: {}".format(text))
            time.sleep(rate_limit)
        return True
    except Exception as e:
        print("Xii... {}".format(e))
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
        tweeting(splitter(text,limit_char=140), rate_limit=2)
    else:
        print("I need some text as parameter")
        sys.exit(1)