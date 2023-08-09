from flask import Flask, request, send_file, send_from_directory
import soundfile as sf
import commons
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import utils
from models import SynthesizerTrn
import torch

# from text_to_speech_model import TextToSpeechModel  # Import model code

app = Flask(__name__)
# tts_model = TextToSpeechModel()  # Khởi tạo mô hình chuyển văn bản thành giọng nói

'''
Generation and save
'''

import time

# start = time.time()
import IPython.display as ipd
import json




# end = time.time()
def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    print("text--:", text_norm)
    return text_norm


# data = request.json  # Nhận dữ liệu văn bản từ yêu cầu POST
text ="xin chào"  # Lấy văn bản từ dữ liệu
config_path = "C:/Users/ADMIN/Desktop/VIT-vn/vits-vn/configs/vietnamese_base.json"

path_to_model = "G:/download/G_last.pth"

hps = utils.get_hparams_from_file(config_path)

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).cpu()

_ = net_g.eval()

net_g, _, _, _ = utils.load_checkpoint(path_to_model, net_g, None)
stn_tst = get_text(text, hps)
with torch.no_grad():
    x_tst = stn_tst.cpu().unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cpu()
    audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate, normalize=False))
sf.write('test.wav', audio, hps.data.sampling_rate)

# Sử dụng mô hình để chuyển văn bản thành giọng nói và lưu thành tệp âm thanh

# Trả về tệp âm thanh cho người dùng
# return text
# return send_from_directory('.', 'temp_audio.wav', as_attachment=True)
# return send_file(audio_path, mimetype='audio/wav')

