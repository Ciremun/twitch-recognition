# twitch-recognition
youtube-dl + SpeechRecognition
get twitch audio stream -> split into segments -> log speech recognition result

## Usage

    python main.py -c <username> [options]

### options

    -l, --language          SpeechRecognition language code
    -e, --engine            SpeechRecognition engine
    -st, --segment-time     ffmpeg segment_time in seconds
    -h, --help              options help

## Install

### requirements

ffmpeg  

#### Python 3

    youtube-dl>=2020.11.1.1
    SpeechRecognition>=3.8.1

### config.json

config default values can be overwritten with options  

`channel`      (str): twitch.tv username  
`language`     (str): language code  
`segment_time` (int): ffmpeg segment_time in seconds  
`engine`       (str): SpeechRecognition engine (Google or Sphinx)  
`targets`      (object of str): key: string to search for, value: response string  
