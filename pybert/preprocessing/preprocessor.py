#encoding:utf-8
import re

replacement = {
    "arent" : "are not",
    "aren't" : "are not",
    "Can’t" : "Cannot",
    "Can't" : "Cannot",
    "can’t" : "cannot",
    "can't" : "cannot",
    "couldn’t" : "could not",
    "couldn't" : "could not",
    "Couldn't" : "Could not",
    "couldnt" : "could not",
    "didn’t" : "did not",
    "didn't" : "did not",
    "doesn’t" : "does not",
    "doesn't" : "does not",
    "don’t" : "do not",
    "don't" : "do not",
    "Don’t" : "Do not",
    "Don't" : "Do not",
    "dont" : "do not",
    "Dont" : "Do not",
    "hadn't" : "had not",
    "hasn't" : "has not",
    "haven't" : "have not",
    "he'd" : "he would",
    "he'll" : "he will",
    "he's" : "he is",
    "he’s" : "he",
    "i'd" : "I would",
    "I’ll" : "I will",
    "I'll" : "I will",
    "i’ll" : "I will",
    "i'll" : "I will",
    "i’m" : "I am",
    "i'm" : "I am",
    "im" : "I am",
    "Im" : "I am",
    "I'm" : "I am",
    "I’m" : "I am",
    "isn't" : "is not",
    "it's" : "it is",
    "It's" : "It is",
    "It`s" : "It is",
    "It’s" : "It is",
    "it'll": "it will",
    "i’ve" : "I have",
    "i've" : "I have",
    "I've" : "I have",
    "let’s" : "let us",
    "Let’s" : "Let us",
    "let's" : "let us",
    "Let's" : "Let us",
    "mightn't" : "might not",
    "mustn't" : "must not",
    "shan't" : "shall not",
    "she'd" : "she would",
    "she'll" : "she will",
    "She'll" : "She will",
    "she's" : "she is",
    "She's" : "She is",
    "shouldn’t" : "should not",
    "shouldn't" : "should not",
    "that's" : "that is",
    "there's" : "there is",
    "they'd" : "they would",
    "they'll" : "they will",
    "they're" : "they are",
    "they’re" : "they are",
    "they've" : "they have",
    "we'd" : "we would",
    "we're" : "we are",
    "We're" : "We are",
    "weren't" : "were not",
    "we've" : "we have",
    "That’s" : "That is",
    "That's" : "That is",
    "what'll" : "what will",
    "what're" : "what are",
    "what's" : "what is",
    "what've" : "what have",
    "where's" : "where is",
    "who'd" : "who would",
    "who'll" : "who will",
    "who're" : "who are",
    "who's" : "who is",
    "who've" : "who have",
    "which’s" : "which is",
    "won't" : "will not",
    "won’t" : "will not",
    "wouldn’t" : "would not",
    "wouldn't" : "would not",
    "you'd" : "you would",
    "you'll" : "you will",
    "you’re" : "you are",
    "you're" : "you are",
    "You're" : "You are",
    "you've" : "you have",
    "you’ve" : "you have",
    "y'all" : "you all",
    "'re" : " are",
    "'em" : "them",
    "wasn’t" : "was not",
    "wasn't" : "was not",
    "we'll" : "we will",
    "tryin'":"trying",
}

class EnglishPreProcessor(object):
    def __init__(self,min_len = 2,stopwords_path = None):
        self.min_len = min_len
        self.stopwords_path = stopwords_path
        self.reset()

    def lower(self,sentence):
        '''
        大写转化为小写
        :param sentence:
        :return:
        '''
        return sentence.lower()

    def reset(self):
        '''
        加载停用词
        :return:
        '''
        if self.stopwords_path:
            with open(self.stopwords_path,'r') as fr:
                self.stopwords = {}
                for line in fr:
                    word = line.strip(' ').strip('\n')
                    self.stopwords[word] = 1


    def clean_length(self,sentence):
        '''
        去除长度小于min_len的文本
        :param sentence:
        :return:
        '''
        if len([x for x in sentence]) >= self.min_len:
            return sentence

    def replace(self,sentence):
        '''
        一些特殊缩写替换
        :param sentence:
        :return:
        '''
        # Replace words like gooood to good
        sentence = re.sub(r'(\w)\1{2,}', r'\1\1', sentence)
        # Normalize common abbreviations
        words = sentence.split(' ')
        words = [replacement[word] if word in replacement else word for word in words]
        sentence_repl = " ".join(words)
        return sentence_repl

    def remove_website(self,sentence):
        '''
        处理网址符号
        :param sentence:
        :return:
        '''
        sentence_repl = re.sub('http\S+', '', sentence)
        #sentence_repl = sentence.replace(r"http\S+", "")
        #sentence_repl = sentence_repl.replace(r"https\S+", "")
        #sentence_repl = sentence_repl.replace(r"http", "")
        #sentence_repl = sentence_repl.replace(r"https", "")
        return sentence_repl

    def remove_name_tag(self,sentence):
        # Remove name tag
        sentence_repl = re.sub('@\S+[\s]*', '', sentence)
        #sentence_repl = sentence.replace(r"@\S+", "")
        return sentence_repl

    def remove_time(self,sentence):
        '''
        特殊数据处理
        :param sentence:
        :return:
        '''
        # Remove time related text
        sentence_repl = sentence.replace(r'\w{3}[+-][0-9]{1,2}\:[0-9]{2}\b', "")  # e.g. UTC+09:00
        sentence_repl = sentence_repl.replace(r'\d{1,2}\:\d{2}\:\d{2}', "")  # e.g. 18:09:01
        sentence_repl = sentence_repl.replace(r'\d{1,2}\:\d{2}', "")  # e.g. 18:09
        # Remove date related text
        # e.g. 11/12/19, 11-1-19, 1.12.19, 11/12/2019
        sentence_repl = sentence_repl.replace(r'\d{1,2}(?:\/|\-|\.)\d{1,2}(?:\/|\-|\.)\d{2,4}', "")
        # e.g. 11 dec, 2019   11 dec 2019   dec 11, 2019
        sentence_repl = sentence_repl.replace(
            r"([\d]{1,2}\s(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s[\d]{1,2})(\s|\,|\,\s|\s\,)[\d]{2,4}",
            "")
        # e.g. 11 december, 2019   11 december 2019   december 11, 2019
        sentence_repl = sentence_repl.replace(
            r"[\d]{1,2}\s(january|february|march|april|may|june|july|august|september|october|november|december)(\s|\,|\,\s|\s\,)[\d]{2,4}",
            "")
        return sentence_repl

    def remove_breaks(self,sentence):
        # Remove line breaks
        sentence_repl = sentence.replace("\r", " ")
        sentence_repl = sentence_repl.replace("\n", " ")
        sentence_repl = re.sub(r"\\n\n", ".", sentence_repl)
        sentence_repl = re.sub('[  ][ ]*', ' ', sentence_repl)
        return sentence_repl

    def remove_ip(self,sentence):
        # Remove phone number and IP address
        sentence_repl = sentence.replace(r'\d{8,}', "")
        sentence_repl = sentence_repl.replace(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', "")
        return sentence_repl

    def adjust_common(self,sentence):
        # Adjust common abbreviation
        sentence_repl = sentence.replace(r" you re ", " you are ")
        sentence_repl = sentence_repl.replace(r" we re ", " we are ")
        sentence_repl = sentence_repl.replace(r" they re ", " they are ") 
        sentence_repl = sentence_repl.replace(r"@", "at")
        sentence_repl = sentence_repl.replace(r"&", "and")
        
        sentence_repl = sentence_repl.replace(r"y'all", "you all")
        sentence_repl = sentence_repl.replace(r"I'm", "I am")
        sentence_repl = sentence_repl.replace(r"You're", "You are")
        sentence_repl = sentence_repl.replace(r"It's", "It is")
        sentence_repl = sentence_repl.replace(r"Couldn't", "Could not")
        
        #sentence_repl = re.sub('![!]+', '!', sentence_repl)
        #sentence_repl = re.sub('\?[\?]+', '?', sentence_repl)
        return sentence_repl

    def remove_chinese(self,sentence):
        # Chinese bad word
        sentence_repl = re.sub(r"fucksex", "fuck sex", sentence)
        sentence_repl = re.sub(r"f u c k", "fuck", sentence_repl)
        
        return sentence_repl

    def full2half(self,sentence):
        '''
        全角转化为半角
        :param sentence:
        :return:
        '''
        ret_str = ''
        for i in sentence:
            if ord(i) >= 33 + 65248 and ord(i) <= 126 + 65248:
                ret_str += chr(ord(i) - 65248)
            else:
                ret_str += i
        return ret_str

    def remove_stopword(self,sentence):
        '''
        去除停用词
        :param sentence:
        :return:
        '''
        words = sentence.split()
        x = [word for word in words if word not in self.stopwords]
        return " ".join(x)

    # 主函数
    def __call__(self, sentence):
        x = sentence
        
        #f = open("data_check.txt", "a")
        #f.write(x)
        #f.write("\n")
        
        # x = self.lower(x)
        
        x = x.replace("’", "'") 
        #x = x.replace("‘", "'")
        #x = x.replace("“", '"')
        #x = x.replace("”", '"')

        x = self.replace(x)
        x = self.remove_website(x)
        x = self.remove_name_tag(x)
        x = self.remove_time(x)
        x = self.remove_breaks(x)
        x = self.remove_ip(x)
        x = self.adjust_common(x)
        x = self.remove_chinese(x)
        
        encoded_string = x.encode("ascii", "ignore")
        decode_string = encoded_string.decode()
        # x = self.lower(x)
        x = decode_string
        
        #f.write(x)
        #f.write("\n")
        #f.write("\n")
        #f.close()
        #x = self.remove_stopword(x)
        return x
