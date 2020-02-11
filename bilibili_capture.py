import requests
import re
from ffmpy3 import FFmpeg
import os


class BiliDownload:
    def __init__(self, url, save_dir=None):
        self.url = url
        self.save_dir = save_dir if save_dir else os.getcwd()

    def download(self):
        hv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/65.0.3325.181 Safari/537.36'}
        response = requests.get(self.url, headers=hv).content.decode('utf-8')
        urls1 = re.findall('"baseUrl":"(.+?)"', response)
        urls2 = re.findall('"url":"(.+?)"', response)
        headers = {
            'Referer': self.url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/65.0.3325.181 Safari/537.36',
            'Range': 'bytes=0-'
        }

        file_name = self.url.split('/')[-1]
        if urls1:
            video = os.path.join(self.save_dir, file_name) + '.mp4'
            audio = os.path.join(self.save_dir, file_name) + '.mp3'
            print('Downloading!')
            with open(video, 'wb') as f:
                f.write(requests.get(urls1[0], headers=headers).content)
            with open(audio, 'wb') as f:
                f.write(requests.get(urls1[-1], headers=headers).content)

            # video audio merge using ffmpeg
            video_merge = os.path.join(self.save_dir, file_name[:8]) + '.mp4'
            ff = FFmpeg(inputs={video: None, audio: None},
                        outputs={video_merge: '-c:v h264 -c:a ac3'})
            ff.run()
            # remove files after merging
            os.remove(video)
            os.remove(audio)

            print('Download complete!')
        elif urls2:
            print('Downloading!')
            video = os.path.join(self.save_dir, file_name) + '.flv'
            with open(video, 'wb') as f:
                f.write(requests.get(urls2[0], headers=headers).content)

            print('Download complete!')


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/av85189907?from=search&seid=10132531973029568910'
    save_dir = '/Users/wangyujue/Downloads'
    cap = BiliDownload(url=url, save_dir=save_dir)
    cap.download()

