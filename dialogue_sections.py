from itertools import chain

'''
这个部分负责从sce提取出可供视频分析校验的列表
'''

class SCEwords:
    #重要的标识符
    title = '［タイトル：'
    sub_title = '［サブタイトル：'
    speaker = '［話：'
    chara_voice = '［Live2Dキャラボイス：'

    fade_in = '［フェードイン：'
    fade_time = 'フェード：'
    close_window = '［ウインドウ非表示：'
    open_window = '［表示：ウインドウ1'
    font_size = '［ウインドウフォントサイズ：'
    jitter_sign = '［ゆれ：ウインドウ1'
    time_identifier = '時間：'
    amplitude_identifier = '幅：'
    live2d_appear = '［Live2Dキャラ表示：'
    
    #需要去除的标识符
    background_name = '［背景DJK：'
    live2d_disappear = '［Live2Dキャラ非表示：'
    live2d_film = '［Live2Dキャラフィルム：'
    bgm_notice = '［音BGM'
    se_notice = '［音SE'
    wait = '［待：'
    sync_start = '［@Parallel：'
    sync_end = '［@End：'
    
    start = '［'
    end = '］\n'
    end_backup = '］' # 涉及索引切片操作的时候用这个

class Event(object):
    def __init__(self, index) -> None:
        self.index = index
        self.event_type = 'Event'

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type}

class Dialogue(Event):
    def __init__(self, index, talker, body) -> None:
        super().__init__(index)
        self.event_type = 'Dialogue'
        self.talker = talker
        self.body = body

    def build_body(self):
        str = '\n'#'\\N'
        return str.join(self.body)

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type, 'Talker':self.talker, 'Body':self.body}

class Title(Event):
    def __init__(self, index, body) -> None:
        super().__init__(index)
        self.event_type = 'Title'
        self.body = body

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type, 'Talker':'Title', 'Body':self.body}

class Subtitle(Event):
    def __init__(self, index, body) -> None:
        super().__init__(index)
        self.event_type = 'Subtitle'
        self.body = body

    def get_dict(self):
        return {'Index':self.index, 'EventType':self.event_type, 'Talker':'Subtitle', 'Body':self.body}
        
class DialogueSections:
    def __clean_text(text:str) -> str:
        li = text.split('＠')
        res = li[0]
        return res

    def __count_nonbracket(li):
        non_bracket = 0
        for l in li:
            if not l.startswith(SCEwords.start):
                non_bracket += 1
        return non_bracket

    def sce_handler(route) -> list:
        '''
        输入sce路径，输出一个包含各节点的列表
        '''
        lees = []
        with open(route, 'r+', encoding='utf-8') as s:
            li = s.readlines()
        
        subli = []
        for l in li:
            if l == '\n':
                lees.append(subli)
                subli = []
            else:
                if l.startswith(SCEwords.background_name):
                    continue
                if l.startswith(SCEwords.live2d_disappear):
                    continue
                if l.startswith(SCEwords.live2d_film):
                    continue
                if l.startswith(SCEwords.bgm_notice):
                    continue
                if l.startswith(SCEwords.se_notice):
                    continue
                if l.startswith(SCEwords.wait):
                    continue
                if l.startswith(SCEwords.sync_start):
                    continue
                if l.startswith(SCEwords.sync_end):
                    continue
                if l.startswith('}'):
                    continue
                if l.startswith('\t'):
                    continue
                else:
                    subli.append(l)
        if subli != []:
            lees.append(subli)
            subli = []

        lis = []
        for lee in lees:
            if lee != []:
                lis.append(lee)

        i = 1
        while i < len(lis):
            if DialogueSections.__count_nonbracket(lis[i]) == 0 and DialogueSections.__count_nonbracket(lis[i-1]) == 0:
                lis[i-1] = list(chain(lis[i-1], lis[i]))
                lis.remove(lis[i])
            if lis[i-1] == lis[-1]:
                break
            i += 1

        event_list = []
        index = 1
        talker = ''

        for block in lis:
            body = []
            for i in range(len(block)):
                line = block[i]

                if line.startswith(SCEwords.title) or line.startswith(SCEwords.sub_title):
                    #判断标题和副标题
                    slic = line.find('：')
                    temp = line.replace(SCEwords.end, '')
                    title_body = temp[slic + 1:]
                    if SCEwords.title in line:
                        tit = Title(index, title_body)
                    else:
                        tit = Subtitle(index, title_body)
                    event_list.append(tit.get_dict())

                if line.startswith('\ufeff{ Main'):
                    continue

                if line.startswith(SCEwords.speaker):
                    temp = line.replace(SCEwords.speaker, '')
                    talker = temp.replace(SCEwords.end, '')

                if line.startswith(SCEwords.chara_voice):
                    temp = line.replace(SCEwords.chara_voice, '')
                    tker = temp.replace(SCEwords.end, '')
                    if tker == talker:
                        talker = tker

                if not line.startswith(SCEwords.start):
                    line = line.replace('\n', '')
                    if '＠' in line:
                        temp = DialogueSections.__clean_text(line)
                        body.append(temp)
                    else:
                        temp = line
                        body.append(temp)

            if body == []:
                continue
            dialogue = Dialogue(index, talker, body)
            dialogue.body = dialogue.build_body()
            event_list.append(dialogue.get_dict())
            index += 1

        return event_list

if __name__ == '__main__':
    pass