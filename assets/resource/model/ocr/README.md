# PaddleOCR model

2023/07/06

from <https://github.com/PaddlePaddle/PaddleOCR/blob/795c81f1835725dbf9bf9f5a13e0c793dfd5f243/doc/doc_en/models_list_en.md>

## det model

ch_PP-OCRv3_det [New] Original lightweight model, supporting Chinese, English, multilingual text detection

<https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar>

## rec model

ch_PP-OCRv3_rec [New] Original lightweight model, supporting Chinese, English, multilingual text recognition

<https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar>

## rec label

<https://github.com/PaddlePaddle/PaddleOCR/blob/795c81f1835725dbf9bf9f5a13e0c793dfd5f243/ppocr/utils/ppocr_keys_v1.txt>

## command

### det

```bash
$ paddle2onnx --model_dir . --model_filename inference.pdmodel --params_filename inference.pdiparams --save_file det_unopt.onnx --opset_version 16 --enable_dev_version True --enable_onnx_checker True --deploy_backend onnxruntime 
[Paddle2ONNX] Start to parse PaddlePaddle model...
[Paddle2ONNX] Model file path: ./inference.pdmodel
[Paddle2ONNX] Paramters file path: ./inference.pdiparams
[Paddle2ONNX] Start to parsing Paddle model...
[Paddle2ONNX] Use opset_version = 16 for ONNX export.
[Paddle2ONNX] PaddlePaddle model is exported as ONNX format now.
2023-07-06 23:36:40 [INFO]      ===============Make PaddlePaddle Better!================
2023-07-06 23:36:40 [INFO]      A little survey: https://iwenjuan.baidu.com/?code=r8hu2s
```

```bash
$ python -m paddle2onnx.optimize --input_model det_unopt.onnx --output_model det.onnx
2023-07-06 23:37:06 [INFO]      Model optmized, saved in det.onnx.
```

### rec

```bash
$ paddle2onnx --model_dir . --model_filename inference.pdmodel --params_filename inference.pdiparams --save_file rec_unopt.onnx --opset_version 16 --enable_dev_version True --enable_onnx_checker True --deploy_backend onnxruntime 
[Paddle2ONNX] Start to parse PaddlePaddle model...
[Paddle2ONNX] Model file path: ./inference.pdmodel
[Paddle2ONNX] Paramters file path: ./inference.pdiparams
[Paddle2ONNX] Start to parsing Paddle model...
[Paddle2ONNX] Use opset_version = 16 for ONNX export.
[Paddle2ONNX] PaddlePaddle model is exported as ONNX format now.
2023-07-06 23:37:28 [INFO]      ===============Make PaddlePaddle Better!================
2023-07-06 23:37:28 [INFO]      A little survey: https://iwenjuan.baidu.com/?code=r8hu2s
```

```bash
$ python -m paddle2onnx.optimize --input_model rec_unopt.onnx --output_model rec.onnx
2023-07-06 23:37:37 [INFO]      Model optmized, saved in rec.onnx.
```
