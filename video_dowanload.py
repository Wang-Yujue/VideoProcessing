import requests
import urllib.request
import os
import subprocess
from pytube import YouTube


class DownloadVideo:
    def __init__(self, url, save_dir, video_format='mp4', res='720p'):
        self.url = url
        self.f = video_format
        self.save_dir = save_dir
        self.res = res

    def download_file(self):
        video_name = self.url.split('/')[-1] + '.' + self.f
        save_d = os.path.join(self.save_dir, video_name)
        r = requests.get(self.url, stream=True)
        with open(save_d, 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)

    def download_from_url(self):
        video_name = self.url.split('/')[-1] + '.' + self.f
        save_d = os.path.join(self.save_dir, video_name)
        urllib.request.urlretrieve(self.url, save_d)

    def download_youtube(self):
        video_name = self.url.split('/')[-1]
        save_d = os.path.join(self.save_dir, video_name)

        yt = YouTube(self.url)
        yt = yt.streams.filter(progressive=True, file_extension=self.f).order_by('resolution').desc().first()
        yt.download(save_d)


class VideoFormatConvert:
    def __init__(self, input_video, target_format='mp4', save_dir=None):
        self.input = input_video
        self.save_dir = save_dir if save_dir else os.getcwd()
        self.target_format = target_format

    def convert_video(self):
        video_input = self.input
        video_name = video_input.split('/')[-1].split['.'][0]
        video_output = os.path.join(self.save_dir, video_name)

        cmd = ['ffmpeg', '-i', video_input, video_output + '.' + self.target_format]
        subprocess.call(cmd)


class VideoConcat:
    def __init__(self, video_dirs, target_format='mp4', save_dir=None):
        self.list = video_dirs
        self.format = target_format
        self.save_dir = save_dir if save_dir else os.getcwd()

    def concat_video(self):
        if not os.path.exists('video_list.txt'):
            with open('video_list.txt', 'w') as f:
                for v in self.list:
                    f.write('file ' + v + '\n')
        else:
            os.remove('video_list.txt')
            with open('video_list.txt', 'w') as f:
                for v in self.list:
                    f.write('file ' + v + '\n')

        cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'video_list.txt',
               '-c', 'copy', 'concatenation.' + self.format]
        subprocess.call(cmd)

        # cmd = ['ffmpeg',
        #        '-i', '屏幕录制2020-02-0709.44.00.mov',
        #        '-i', '屏幕录制2020-02-0710.05.55.mov',
        #        '-i', '屏幕录制2020-02-0710.20.29.mov',
        #        '-i', 'av851899.mp4',
        #        '-i', '屏幕录制2020-02-0710.35.13.mov',
        #        '-filter_complex',
        #        '[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0][3:v:0][3:a:0][4:v:0][4:a:0]concat=n=5:v=1:a=1[outv][outa]',
        #        '-map', '[outv]', '-map', '[outa]', 'concatenation.mp4'
        #        ]
        # subprocess.call(cmd)


if __name__ == '__main__':
    save_directory = '/Users/wangyujue/Downloads'

    # input_video = ''
    # video_convert = VideoFormatConvert(input_video=input_video, target_format='mp4', save_dir=None)
    # video_convert.convert_video()

    video_dirs = ['/Users/wangyujue/Documents/PycharmProjects/VideoProcessing/屏幕录制2020-02-0709.44.00.mov',
                  '/Users/wangyujue/Documents/PycharmProjects/VideoProcessing/屏幕录制2020-02-0710.05.55.mov',
                  '/Users/wangyujue/Documents/PycharmProjects/VideoProcessing/屏幕录制2020-02-0710.20.29.mov',
                  '/Users/wangyujue/Documents/PycharmProjects/VideoProcessing/屏幕录制2020-02-0710.27.10.mov',
                  '/Users/wangyujue/Documents/PycharmProjects/VideoProcessing/屏幕录制2020-02-0710.35.13.mov'
                  ]
    video_concat = VideoConcat(video_dirs=video_dirs, target_format='mp4')
    video_concat.concat_video()




