import argparse
import os

import text
from utils import load_filepaths_and_text

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--out_extension", default="cleaned")
  parser.add_argument("--text_index", default=1, type=int)
  parser.add_argument("--filelists", nargs="+", default=["filelists/vivos_train_filelist.txt", "filelists/vivos_val_filelist.txt"])
  parser.add_argument("--text_cleaners", nargs="+", default=["vietnamese_cleaners"])

  args = parser.parse_args()
    

  for filelist in args.filelists:
    print("START:", filelist)
    filepaths_and_text = load_filepaths_and_text(filelist)
    for i in range(len(filepaths_and_text)):
      original_text = filepaths_and_text[i][args.text_index]
      cleaned_text = text._clean_text(original_text, args.text_cleaners)
      filepaths_and_text[i][args.text_index] = cleaned_text
    # Đường dẫn thư mục đích để lưu các tệp mới
    output_directory = "/content/drive/MyDrive/Vinbigdata/trainsmall"

    # Lấy tên tệp gốc
    original_file_name = os.path.basename(filelist)

    # Tạo tên tệp mới bằng cách thêm phần mở rộng chỉ định vào tên tệp gốc
    new_file_name = original_file_name + "." + args.out_extension

    # Tạo đường dẫn đầy đủ của tệp mới
    new_file_path = os.path.join(output_directory, new_file_name)

    # Ghi dữ liệu vào tệp mới
    with open(new_file_path, "w", encoding="utf-8") as f:
      f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])