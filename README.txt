Rice Model API
===============

Files:
- predict_api.py        # Flask app exposing /predict
- DenseNet121_rice_model.h5   # placeholder (will be created by training script)
- MobileNet_rice_model.h5     # placeholder
- requirements.txt
- train_models.py       # training script (use dataset folder)
- uploads/              # saved incoming files

Steps:
1. (Optional) Train models using train_models.py. Provide dataset in folders:
   dataset/train/<class>/... and dataset/val/<class>/...
   Classes: Basmati, Sona_Masuri, Ponni, IR64, Jasmine
2. Install dependencies: pip install -r requirements.txt
3. Run: python predict_api.py
4. Make sure Flask runs on 127.0.0.1:5000 so PHP can call it.
