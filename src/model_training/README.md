# Training

Tại function này, các model load data từ hopswork dưới dạng data frame, import vào model và thực hiện training. Kết quả là một model hoàn chỉnh được lưu dưới dạng `pickle` file, hai file json lưu model artifact và model evaluate. Cả ba file này được lưu tại thư mục `./data/models/`.

Các file trả về cần có tên với format như sau:
- {dataset_name} + "\_" + {dataset_version} + "\_" + {model_name} + ".pkl"
- {dataset_name} + "\_" + {dataset_version} + "\_" + {model_name} + ".json"
- "eval_" + {dataset_name} + "\_" + {dataset_version} + "\_" + {model_name} + ".json"