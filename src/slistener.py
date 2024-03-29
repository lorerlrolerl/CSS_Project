import tweepy
from tweepy import StreamListener
import json, time, sys

class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        #self.output  = open(fprefix + '.' 
        #                    + time.strftime('%Y%m%d-%H%M%S') + '.txt', 'w')
        #self.hashes  = open(fprefix + 'hashes.' 
        #                    + time.strftime('%Y%m%d-%H%M%S') + '.txt', 'w')
        self.delout  = open('delete.txt', 'a')

    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status(self, status):
        #self.output.write(str(status.created_at)+ '\t'+  str(status.retweet_count) + '\t'+str(status.favorite_count) + '\n')
        print status.created_at
        #self.output.write(status.__getstate__().created_at+'\n')
        #hashtags = status.entities['hashtags']
        #for hashtag in hashtags:
            #print hashtag['text'].lower()
            #teamhashes.append(hashtag['text'].lower())
            #self.hashes.write(hashtag['text'].lower())
        '''self.counter += 1

        if self.counter >= 200000:
            self.output.close()
            self.output = open('../streaming_data/' + self.fprefix + '.' 
                               + time.strftime('%Y%m%d-%H%M%S') + '.txt', 'w')
            #self.hashes = open('../streaming_data/hashes' + self.fprefix + '.' 
            #                   + time.strftime('%Y%m%d-%H%M%S') + '.txt', 'w')
            self.counter = 0
        '''
        #return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 
