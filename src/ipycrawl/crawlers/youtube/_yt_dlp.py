# -*- coding: utf-8 -*-

# GITHUB : https://github.com/yt-dlp/yt-dlp
# PYPI : https://pypi.org/project/yt-dlp/
# DOC : 
# pip install yt-dlp
# pip install ffmpeg
# 정상동작 확인일 : 2024-12-28 



import json 
import subprocess
import re 
import os 


import yt_dlp




FFMPEG_LOCATION = os.environ['FFMPEG_BIN_LOCATION']

VIDEO_DOWNLOAD_PATH = os.environ['YOUTUBE_VIDEO_DOWNLOAD_PATH']
AUDIO_DOWNLOAD_PATH = os.environ['YOUTUBE_AUDIO_DOWNLOAD_PATH']
AUDIO_DOWNLOAD_GOOGLE_PATH = os.environ['YOUTUBE_AUDIO_DOWNLOAD_GOOGLE_PATH']


# ============================================================
# TESTs 
# ============================================================


def download_video(url):
# Replace this URL with the YouTube video you want to download

    try:
        # Create an instance of YoutubeDL
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print('Download completed successfully.')

    except Exception as e:
        print(f'An error occurred: {e}')





def download_info(url, jsonfile):
    info = extract_information(url)
    with open(jsonfile, 'w') as f:
        f.write(json.dumps(info))
        f.close() 
    print('DONE.')


def extract_audio(url):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
    
    print('DONE.')


def download_audio_files_from_playlist(url):
    # url ="https://www.youtube.com/playlist?list=PL_a1wRn79us-7t6zoK90sUrqM7RIG1qAR" 
    # command = f'yt-dlp -x --audio-format mp3 --audio-quality 320k --ffmpeg-location \"{FFMPEG_LOCATION}\" --yes-playlist {url}'
    # command = generate_command(url, type='audio')
    command = generate_command_v2(url, options=default_audio_options(), only_audio=True)
    subprocess.call(command, shell=True)
    
    print('DONE.')



# ============================================================
# FINAL APIs
# ============================================================

# 오디오 옵션 생성
def default_audio_options(format='mp3', quality='320k'):
    return {
        '--audio-format': 'mp3',
        '--audio-quality': '320k',
    }

def extract_information(url):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # print('\nINFORMATION-->', type(info), info)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        info = ydl.sanitize_info(info)
        # print('\n깨끗한-->', type(info), info)

    return info 


def generate_command(url, type='video', output=None, outpath=None):
    # 샘플
    # command = f'yt-dlp -x --audio-format mp3 --audio-quality 320k --ffmpeg-location \"{FFMPEG_LOCATION}\" --yes-playlist {url}'

    command = 'yt-dlp'
    options = {}

    if type == 'video':
        options.update({
            '-f': 'bestvideo*+bestaudio/best',
            '--merge-output-format': 'mp4',
        })
    if type == 'audio':
        command += ' -x'
        options.update({
            '--audio-format': 'mp3',
            '--audio-quality': '320k',
        })

    # 공통적용 옵션들
    output = f"%(title)s.%(ext)s" if output is None else output 
    options.update({
        '--ffmpeg-location': FFMPEG_LOCATION,
        '-o': output,
    })
    if outpath is not None:
        options.update({"-P": outpath})


    m = re.search('/playlist?', url)
    if m is not None:
        options.update({"--yes-playlist": url})

    # 커멘드에 옵션들 넣기 
    for k,v in options.items():
        command = command + " " + k + " " + v

    # 맨마지막에 URL 삽입
    if m is None:
        command += " " + url 
    else:
        pass 
    
    print('\nCOMMAND-->\n', command)    
    return command 

def generate_command_v2(url, options, only_audio=False, output=None, outpath=None):
    # 샘플
    # command = f'yt-dlp -x --audio-format mp3 --audio-quality 320k --ffmpeg-location \"{FFMPEG_LOCATION}\" --yes-playlist {url}'

    command = 'yt-dlp'

    if only_audio:
        command += ' -x'

    # 공통적용 옵션들
    output = f"%(title)s.%(ext)s" if output is None else output 
    outdir = AUDIO_DOWNLOAD_PATH if outpath is None else outpath
    options.update({
        '--ffmpeg-location': FFMPEG_LOCATION,
        '-o': output,
        '-P': outdir,
    })


    m = re.search('/playlist?', url)
    if m is not None:
        options.update({"--yes-playlist": url})

    # 커멘드에 옵션들 넣기 
    for k,v in options.items():
        command = command + " " + k + " " + v

    # 맨마지막에 URL 삽입
    if m is None:
        command += " " + url 
    else:
        pass 
    
    print('\nCOMMAND-->\n', command)    
    return command 


def print_info(url):
    info = extract_information(url)
    print('-'*100)
    print('YouTube ID:', info['id'])
    print('Title:', info['title'])
    return info 



def download_audio(url, output=None, outpath=None):
    # 오디오 옵션 생성
    options = {
        '--audio-format': 'mp3',
        '--audio-quality': '320k',
    }

    # 음악장르에 따라 폴더 구분을 어떻게 할지

    # 구글드라이브로 이동
    info = print_info(url)
    filename = info['title']+'.mp3'
    srcfile = os.path.join(outpath, filename)
    dstfile = os.path.join(AUDIO_DOWNLOAD_GOOGLE_PATH, filename)
    
    command = generate_command_v2(url, options, only_audio=True, output=output, outpath=outpath)
    subprocess.call(command, shell=True)

    # 구글드라이브로 이동
    try:
        os.rename(srcfile, dstfile)
    except OSError as e:
        print(f'ERROR | {e}')
        print('SRC-->', srcfile)
        print('DST-->', dstfile)
    
    print('DONE.')


def clean_outpath(s):
    s = re.sub('\s*\|\s*', repl='__', string=s)
    return re.sub('\s', repl='_', string=s)


def download_video(url, output=None, outpath=None, mkdir=False):
    # command = f'yt-dlp -f bestvideo*+bestaudio/best --ffmpeg-location \"{FFMPEG_LOCATION}\" -o "%(title)s.%(ext)s" https://www.youtube.com/watch?v=Jrmb07ku6ZY&ab_channel=CristianyGabriella'
    if mkdir and isinstance(outpath, str):
        # info = extract_information(url)
        info = print_info(url)
        _dir = clean_outpath(info['title'])
        outpath = os.path.join(outpath, _dir)
        os.makedirs(outpath, exist_ok=True)
    else:
        pass 

    # 비디오 옵션 생성
    options = {
        '-f': 'bestvideo*+bestaudio/best',
        '--merge-output-format': 'mp4',
    }

    command = generate_command_v2(url, options, output=output, outpath=outpath)
    subprocess.call(command, shell=True)
    
    print('DONE.')








