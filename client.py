# -*- coding: utf-8 -*-
import requests
import json
import struct
import time
import uuid
import os
import base64
import numpy as np


s0 = '没有听到喔，镜子的英文是什么？'
s1 = 'how are you, how old are you?'
s2 = '苹果的英文是：apple，a-p-p-l-e，apple'
s3 = '苹果的英文是：apple,a-p-p-l-e,apple'
s4 = '阿基米德说过，给我一个apple，我能吃一整天'
s5 = '小朋友跳的真自信，很棒。抖抖腿放松放松，比对结果马上就出来啦'
input_text = s0
rqt_url = 'http://60.205.178.158:10027/tts/getText'
#rqt_url = 'aiwifi.tts-beta.tuling123.com/tts/getText'
# szx_16k
# rqt_url = 'http://47.94.2.191:10025/tts/getText'
# rqt_url = 'http://60.205.178.158:10025/tts/getText'
# rqt_url = 'http://tts-universe.tuling123.com/tts/getText'

# xtc_16k
# rqt_url = 'http://47.94.2.191:10013/tts/getText'
# rqt_url = 'http://60.205.178.158:10013/tts/getText'
# rqt_url = 'http://xiaotiancai-tts.tuling123.com/tts/getText'

# zhiwa_16k
# rqt_url = 'http://47.94.2.191:10023/tts/getText'
# rqt_url = 'http://60.205.178.158:10023/tts/getText'
# rqt_url = 'http://zhiwa1-tts.tuling123.com/tts/getText'

# emotion_16k
#rqt_url = 'http://47.94.2.191:10029/tts/getText'
# rqt_url = 'http://60.205.178.158:10029/tts/getText'
# rqt_url = 'http://emotion1-tts.tuling123.com/tts/getText'

# ht_16k
# rqt_url = 'http://47.94.2.191:10012/tts/getText'
# rqt_url = 'http://60.205.178.158:10012/tts/getText'
# rqt_url = 'http://general-tts.tuling123.com/tts/getText'

# iqy_24k
# rqt_url = 'http://47.94.2.191:10003/tts/getText'
# rqt_url = 'http://60.205.178.158:10003/tts/getText'
# rqt_url = 'http://iqiyitts01.tuling123.com/tts/getText'

# zhiwa_24k
# rqt_url = 'http://47.94.2.191:10024/tts/getText'
# rqt_url = 'http://60.205.178.158:10024/tts/getText'
# rqt_url = 'http://zhiwa2-tts.tuling123.com/tts/getText'

# emotion_24k
# rqt_url = 'http://47.94.2.191:10005/tts/getText'
# rqt_url = 'http://60.205.178.158:10005/tts/getText'
# rqt_url = 'http://emotion-tts.tuling123.com/tts/getText'
# rqt_url = 'http://emotion-tts.demo.tuling123.com/tts/getText'


# ht_24k
# rqt_url = 'http://47.94.2.191:10028/tts/getText'
# rqt_url = 'http://60.205.178.158:10028/tts/getText'
# rqt_url = 'http://huiting2-tts-demo.turingapi.com/tts/getText'

# domain name for 'http://47.94.2.191:10012/tts/getText'
#rqt_url = 'http://general-tts.tuling123.com/tts/getText'


# zhiwa_8k
# rqt_url = 'http://47.94.2.191:10035/tts/getText'
#rqt_url = 'http://zhiwa8-tts.tuling123.com/tts/getText'

# emotion_8k
# rqt_url = 'http://47.94.2.191:10036/tts/getText'
# rqt_url = 'http://emotion8-tts.tuling123.com/tts/getText'

# ht_8k
#rqt_url = 'http://47.94.2.191:10037/tts/getText'
# rqt_url = 'http://huiting8-tts.turingapi.com/tts/getText'


def string_to_pcm(pcm_string):
    # input format, the last comma is essential: '3,5,6,9,-5,'
    pcm_list = pcm_string[0:len(pcm_string)-1].split(',')
    pcm_list = [int(i) for i in pcm_list]
    return pcm_list


def parse_response(buff, encode_format):
    json_obj = json.loads(buff)
    ret = json_obj['ret']
    if ret < 0:
        return None
    else:
        index = json_obj['index']
        if index == -1:
            return []
        else:
            if encode_format == 'base64':
                pcm_base64 = base64.decodestring(json_obj['data'])
                pcm = np.frombuffer(pcm_base64, dtype=np.int16)
                return pcm
            else:
                return string_to_pcm(json_obj['data'])


def write_to_file(pcm_list, fp):
    for p in pcm_list:
        # write as short
        fp.write(struct.pack('h', p))


def post_request(url, text, encode_fmt, output_pcm, track_key, is_stream=False, is_szx=False, fast_mode=False):
    rqt_dict = dict()
    rqt_dict['text_str'] = text
    rqt_dict['encode_fmt'] = encode_fmt
    rqt_dict['stream'] = int(is_stream)
    rqt_dict['track_key'] = track_key
    rqt_dict['syl_flag'] = int(is_szx)
    rqt_dict['fast_mode'] = int(fast_mode)

    rqt_dict['punc_len'] = '100,200,300,400'

    
    rqt_header = {'Content-type': 'application/json'}
    #print json.dumps(rqt_dict)
    ff = open(output_pcm, 'wb')
    try:
        is_first = True
        t1 = time.time()
        response = requests.post(url=url, data=json.dumps(rqt_dict), headers=rqt_header, stream=True)
        if response.ok is False:
            print '(%s) response not ok' % track_key
        else:
            for buf in response.iter_lines():

                # with open('response.txt', 'a+') as rf:
                #     rf.write(buf+'\n')
                # print len(buf), buf

                #print len(buf), buf

                if is_szx:
                    continue
                pcm = parse_response(buf, encode_fmt)
                if pcm is None:  # error occurred
                    #print buf
                    break
                else:
                    if len(pcm) == 0:  # reach the end
                        final_batch_time = time.time()-t1
                        break
                    else:
                        write_to_file(pcm, ff)  # normal branch
                        if is_first:
                            first_batch_time = time.time()-t1
                            is_first = False
    except:
        print '(%s) exception' % track_key
    ff.close()
    return first_batch_time, final_batch_time


# rqt_url = 'http://test-tts.tuling123.com/tts/getText'

#rqt_url = 'http://192.168.50.9:10034/tts/getText'
## rqt_url = 'http://47.94.2.191:10035/tts/getText'

#rqt_url = 'http://192.168.50.9:10025/tts/getText'
# rqt_url = 'http://192.168.50.16:10030/tts/synthesis'
# rqt_url = 'http://192.168.10.165:10005/tts/getText'

b_batch_test = False
num_samples = 1000


if not b_batch_test:
    for k, v in {0: s0, 1: s1, 2: s2, 3: s3, 4: s4}.items():
        unique_key = str(uuid.uuid1())
        pcm_name = 's%d.pcm' % k
        t_first, t_final = post_request(url=rqt_url,
                                        text=v,
                                        encode_fmt='base64',
                                        output_pcm=pcm_name,
                                        track_key=unique_key,
                                        is_stream=False,
                                        is_szx=False,
                                        fast_mode=False)

        print '(%s): A=%f B=%f %s' % (unique_key, t_first, t_final, pcm_name)
        os.system('play -t raw -r 8k -e signed -b 16 -c 1 %s' % pcm_name)
else:
    first_time_list = []
    final_time_list = []
    for i in range(num_samples):
        unique_key = str(uuid.uuid1())
        pcm_name = 's0.pcm'
        t_first, t_final = post_request(url=rqt_url,
                                        text=s0,
                                        encode_fmt='base64',
                                        output_pcm=pcm_name,
                                        track_key=unique_key,
                                        is_stream=False,
                                        is_szx=False,
                                        fast_mode=False)
        print '(%05d) (%s): A=%f B=%f %s' % (i, unique_key, t_first, t_final, pcm_name)
        first_time_list.append(t_first)
        final_time_list.append(t_final)

    first_time_list.sort()
    final_time_list.sort()
    print '70%%: %f %f' % (first_time_list[int(num_samples*0.70)], final_time_list[int(num_samples*0.70)])
    print '80%%: %f %f' % (first_time_list[int(num_samples*0.80)], final_time_list[int(num_samples*0.80)])
    print '90%%: %f %f' % (first_time_list[int(num_samples*0.90)], final_time_list[int(num_samples*0.90)])
    print '95%%: %f %f' % (first_time_list[int(num_samples*0.95)], final_time_list[int(num_samples*0.95)])
    print '99%%: %f %f' % (first_time_list[int(num_samples*0.99)], final_time_list[int(num_samples*0.99)])
    for t in first_time_list:
        print t,
    print
    for t in final_time_list:
        print t,











