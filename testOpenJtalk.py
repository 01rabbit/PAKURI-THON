# install
# sudo apt install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001

import subprocess

def jtalk(str):
    # -x : 辞書ディレクトリの指定
    # -m : 音声エンジンの指定
    # -r : 音声スピードの指定
    # -ow: 音声出力結果の保存ファイル(上書き)
    open_jtalk = ['open_jtalk',
                  '-x','/var/lib/mecab/dic/open-jtalk/naist-jdic',
                  '-m','/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice',
                  '-r','1.5',
                  '-ow','sample_jtalk.wav']
    subprocess.run(open_jtalk, input=str.encode())

    # 音声再生
    aplay = ['aplay',
             '-t','wav',
             'sample_jtalk.wav']
    subprocess.run(aplay)

# talkメソッド
def talk():
    text = 'チケットの料金は、12,345円です。'
    text += 'OK, thank you.'
    jtalk(text)

# main
if __name__ == '__main__':
    talk()