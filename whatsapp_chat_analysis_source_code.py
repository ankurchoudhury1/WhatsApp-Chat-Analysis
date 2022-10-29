TCONV = {1:13, 2:14, 3:15, 4:16, 5:17, 6:18, 7:19, 8:20, 9:21, 10:22, 11:23, 12:0}
PATTERN_DATE = [("\d+\/\d+\/\d+, \d+:\d+ -"), ("\d+\/\d+\/\d+, \d+:\d+ [apAP]m -")]
PATTERN_IGNORE = "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp,"

def date_as_12_hr(file):
    with open(file, 'r', encoding='utf-8') as file:
        G = []
        author = ""
        date = ""
        time = ""
        msg = "GGG"
        for l in file:
            x = re.search(PATTERN_DATE[1], l) 
            if(x):
                date_time_all = l.split(" - ")[0].split(", ")
                date = date_time_all[0]
                time = date_time_all[1]
                if(time[-2] == ('p' or 'P')):
                    hr = time.split(':')[0].replace(time.split(':')[0], str(TCONV[int(time.split(':')[0])]))
                    time = hr + ':' + time.split(" ")[0].split(":")[1]
                else:
                    time = time.split(" ")[0]     
                author_msg_all = l[len(x.group())::]
                author_msg = re.split(": ", author_msg_all)
                if(len(author_msg)>1):
                    author = author_msg[0]
                    msg = author_msg_all[len(author):]
                else:
                    author = ''
                    msg = author_msg[0]      
            else:
                author = author
                msg = l    
            G.append([date.strip(), time.strip(), author.strip(), msg.strip()])
        return np.array(G)

def date_as_24_hr(file):
    with open(file, 'r', encoding='utf-8') as file:
        G = []
        author = ""
        date = ""
        time = ""
        msg = "TTT"
        for l in file:
            x = re.search(PATTERN_DATE[0], l)
            if(x):
                date_time_all = l[0:len(x.group())]
                date_time = date_time_all.split(', ')
                date = date_time[0]
                time = date_time[1][:-1]
                author_msg_all = l[len(x.group())::]
                author_msg = re.split(': ', author_msg_all)
                if(len(author_msg)>1):
                    author = author_msg[0]
                    msg = author_msg_all[len(author):]
                else:
                    author = ''
                    msg = author_msg[0]
            else:
                author = author
                msg = l        
            G.append([date.strip(), time.strip(), author.strip(), msg.strip()])
        return np.array(G)

def load(F):
    with open(F, encoding='utf-8') as file:
        if (re.search(PATTERN_DATE[0], file.readline())):
            return date_as_24_hr(F)
        else:
            return date_as_12_hr(F)

def make_df(x):
    df = pd.DataFrame(load(x), columns=['Date', "Time", 'Author', 'Msg'])
    df['Hour'] = df['Time'].str.split(':').str[0]
    df['Year'] = pd.DatetimeIndex(df['Date']).year   
    df = df.astype({'Date':'category',
                'Time':'category',
                'Author':'category',
                'Msg': 'category',
                'Hour': 'int',
                'Year': 'int',
               }) 
    return df