# 🎯 Model Training Guide

Complete guide for retraining models in the MusicAITools ecosystem.

## 🎼 Available Models for Training

### 1. **InstrumentTimbre Model** 
- **Purpose**: Chinese traditional instrument timbre analysis and conversion
- **Location**: `InstrumentTimbre/`
- **Training Script**: `train.py`
- **Model File**: `saved_models/model.pt`

### 2. **Theory Net Emotion Model**
- **Purpose**: Music emotion analysis with 10 emotion categories
- **Location**: `theory_net/`
- **Training Script**: `train/train_emotion_model.py`
- **Model File**: `models/models/emotion_model.pt`

### 3. **Theory Net Music Theory Model**
- **Purpose**: Music theory analysis (harmony, rhythm, key detection)
- **Location**: `theory_net/`
- **Training Script**: `train/train_theory_model.py`
- **Model File**: `models/models/theory_model.pt`

---

## 🛠️ Training Setup

### Prerequisites

```bash
# 1. Activate environment
conda activate myenv

# 2. Ensure all dependencies are installed
pip install -r requirements.txt

# 3. Prepare training data
# Place your audio files in appropriate directories
```

### Training Data Structure

```
MusicAITools/
├── wav/                    # General audio files
├── InstrumentTimbre/
│   └── data/
│       └── samples/        # Instrument samples
└── theory_net/
    └── datasets/           # Emotion/theory labeled data
```

---

## 🎵 Training InstrumentTimbre Model

### Quick Start

```bash
cd InstrumentTimbre

# Basic training with default settings
python train.py --data-dir ../wav --epochs 50

# Chinese instruments specialized training
python train.py \
    --chinese-instruments \
    --data-dir ../wav \
    --epochs 100 \
    --batch-size 16 \
    --lr 0.0001 \
    --feature-type multi
```

### Advanced Configuration

```bash
# Full feature training
python train.py \
    --data-dir ../wav \
    --model-path ./saved_models/custom_model.pt \
    --chinese-instruments \
    --use-wav-files \
    --augment \
    --epochs 200 \
    --batch-size 32 \
    --lr 0.001 \
    --patience 10 \
    --cache-features \
    --pretrained \
    --export-onnx \
    --device auto
```

### Parameters Explained

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `--data-dir` | Training data directory | `../wav` | Any path |
| `--epochs` | Training epochs | 30 | 1-1000 |
| `--batch-size` | Batch size | 32 | 8-128 |
| `--lr` | Learning rate | 0.001 | 0.0001-0.01 |
| `--chinese-instruments` | Optimize for Chinese instruments | False | Flag |
| `--feature-type` | Feature extraction type | `multi` | mel, constant-q, multi |
| `--augment` | Apply data augmentation | False | Flag |
| `--pretrained` | Use pretrained weights | False | Flag |

### Training Output

```
Using device: cuda
Using specialized data loader for Chinese traditional instruments
Starting model training...
Epoch 1/100: Loss=0.245, Accuracy=0.876
Epoch 2/100: Loss=0.189, Accuracy=0.912
...
Training complete!
Model saved to ./saved_models/model.pt
```

---

## 🎭 Training Emotion Analysis Model

### Quick Start

```bash
cd theory_net

# Basic emotion model training
python train/train_emotion_model.py \
    --audio-dir ../wav \
    --epochs 100 \
    --batch-size 32
```

### Advanced Training

```bash
# Comprehensive emotion training
python train/train_emotion_model.py \
    --audio-dir ../wav \
    --model-save-path ./models/models/emotion_model_v2.pt \
    --epochs 200 \
    --batch-size 16 \
    --learning-rate 0.0001 \
    --validation-split 0.2 \
    --early-stopping-patience 15 \
    --augment-data \
    --use-pretrained \
    --device cuda
```

### Emotion Categories

The model trains on 10 emotion categories:
1. Happy (快乐)
2. Sad (悲伤) 
3. Angry (愤怒)
4. Peaceful (平静)
5. Energetic (充满活力)
6. Melancholic (忧郁)
7. Romantic (浪漫)
8. Mysterious (神秘)
9. Dramatic (戏剧性)
10. Relaxed (放松)

---

## 🎼 Training Music Theory Model

### Quick Start

```bash
cd theory_net

# Basic theory model training
python train/train_theory_model.py \
    --data-dir ../wav \
    --epochs 150
```

### Advanced Configuration

```bash
# Complete theory analysis training
python train/train_theory_model.py \
    --data-dir ../wav \
    --model-save-path ./models/models/theory_model_v2.pt \
    --epochs 300 \
    --batch-size 24 \
    --learning-rate 0.001 \
    --include-harmony \
    --include-rhythm \
    --include-key-detection \
    --validation-split 0.15 \
    --scheduler-step-size 50 \
    --scheduler-gamma 0.5
```

---

## 📊 Training Data Preparation

### 1. **For InstrumentTimbre Model**

```bash
# Organize instrument samples
mkdir -p InstrumentTimbre/data/samples
cp your_instrument_files/*.wav InstrumentTimbre/data/samples/

# Supported instruments:
# - erhu (二胡)
# - pipa (琵琶) 
# - guzheng (古筝)
# - dizi (笛子)
# - piano, guitar, violin, etc.
```

### 2. **For Emotion Model**

```python
# Create emotion labels file
# theory_net/datasets/labels.json
{
    "audio1.wav": "happy",
    "audio2.wav": "sad",
    "audio3.wav": "peaceful",
    ...
}
```

### 3. **For Theory Model**

```python
# Create theory labels file  
# theory_net/datasets/theory_labels.json
{
    "song1.wav": {
        "key": "C_major",
        "tempo": 120,
        "time_signature": "4/4",
        "chord_progression": ["C", "Am", "F", "G"]
    },
    ...
}
```

---

## 📈 Monitoring Training Progress

### 1. **Training Logs**

```bash
# Monitor training in real-time
tail -f training.log

# Look for key metrics
grep -E "(Loss|Accuracy|Validation)" training.log
```

### 2. **TensorBoard (if available)**

```bash
# Start TensorBoard
tensorboard --logdir=./logs

# View in browser
http://localhost:6006
```

### 3. **Model Checkpoints**

```bash
# Models are automatically saved
ls -la saved_models/
ls -la theory_net/models/models/

# Best model selection
# Models with lowest validation loss are typically best
```

---

## 🎯 Custom Training Scripts

### Create Custom Training Pipeline

```python
#!/usr/bin/env python3
"""
Custom training script for your specific needs
"""

import sys
from pathlib import Path

# Add to path
sys.path.append(str(Path(__file__).parent.parent))

from InstrumentTimbre.models.model import InstrumentTimbreModel
from theory_net.models.emotion_model import EmotionModel

def train_custom_model():
    """Train model with your specific configuration"""
    
    # 1. Prepare your data
    data_dir = "path/to/your/audio/files"
    
    # 2. Initialize model
    model = InstrumentTimbreModel(
        chinese_instruments=True,
        feature_caching=True,
        device='cuda'
    )
    
    # 3. Prepare data loader
    from InstrumentTimbre.utils.data import prepare_chinese_instrument_dataloader
    
    dataloader = prepare_chinese_instrument_dataloader(
        data_dir,
        batch_size=16,
        augment=True,
        feature_type='multi'
    )
    
    # 4. Train
    model.train(
        dataloader=dataloader,
        epochs=100,
        learning_rate=0.0001
    )
    
    # 5. Save
    model.save_model("custom_model.pt")

if __name__ == "__main__":
    train_custom_model()
```

---

## 🔧 Training Optimization Tips

### 1. **Hardware Optimization**

```bash
# Check GPU availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Monitor GPU usage during training
nvidia-smi -l 1

# Use mixed precision for faster training
--use-amp  # if supported
```

### 2. **Data Augmentation**

```python
# Automatic augmentation options
--augment  # Enables:
# - Pitch shifting
# - Time stretching  
# - Noise addition
# - Volume scaling
# - Reverb effects
```

### 3. **Hyperparameter Tuning**

```bash
# Learning rate scheduling
--scheduler-step-size 30 --scheduler-gamma 0.1

# Early stopping
--patience 10

# Batch size optimization
--batch-size 16  # Start smaller, increase if memory allows
```

### 4. **Training Resume**

```python
# Most training scripts support resuming
--resume-from-checkpoint saved_models/checkpoint_epoch_50.pt
```

---

## 📊 Evaluation and Validation

### 1. **Model Testing**

```bash
# Test trained InstrumentTimbre model
cd InstrumentTimbre
python -c "
from models.model import InstrumentTimbreModel
model = InstrumentTimbreModel()
model.load_model('saved_models/model.pt')
# Test with your audio files
"
```

### 2. **Performance Metrics**

```python
# Check model performance
python evaluate_model.py \
    --model-path saved_models/model.pt \
    --test-data ../wav \
    --metrics accuracy,precision,recall,f1
```

### 3. **Cross-Validation**

```bash
# K-fold cross validation
python train.py --k-fold 5 --epochs 50
```

---

## 🚀 Advanced Training Strategies

### 1. **Transfer Learning**

```bash
# Start from pretrained model
python train.py \
    --pretrained \
    --freeze-backbone \
    --fine-tune-epochs 50
```

### 2. **Multi-GPU Training**

```bash
# Distributed training (if multiple GPUs)
python -m torch.distributed.launch \
    --nproc_per_node=2 \
    train.py --distributed
```

### 3. **Ensemble Training**

```bash
# Train multiple models for ensemble
for i in {1..5}; do
    python train.py \
        --model-path saved_models/ensemble_model_$i.pt \
        --random-seed $i
done
```

---

## 🎉 Quick Training Examples

### Example 1: Retrain for Your Instrument Collection

```bash
# Prepare your audio files
mkdir -p my_instruments
cp /path/to/your/audio/*.wav my_instruments/

# Train specialized model
cd InstrumentTimbre
python train.py \
    --data-dir ../my_instruments \
    --chinese-instruments \
    --epochs 100 \
    --augment \
    --model-path saved_models/my_custom_model.pt
```

### Example 2: Emotion Model for Your Music Style

```bash
# Prepare labeled emotion data
# Create labels.json with your music files and emotions

cd theory_net
python train/train_emotion_model.py \
    --audio-dir ../my_music \
    --epochs 200 \
    --batch-size 16 \
    --augment-data
```

### Example 3: Quick Prototype Training

```bash
# Fast training for testing
python train.py \
    --data-dir ../wav \
    --epochs 10 \
    --batch-size 8 \
    --debug
```

---

## 🛠️ Troubleshooting Training Issues

### Common Problems

1. **Out of Memory Error**
   ```bash
   # Reduce batch size
   --batch-size 8
   
   # Enable gradient checkpointing
   --gradient-checkpointing
   ```

2. **Slow Training**
   ```bash
   # Enable feature caching
   --cache-features
   
   # Use smaller model
   --model-size small
   ```

3. **Poor Convergence**
   ```bash
   # Adjust learning rate
   --lr 0.0001
   
   # Increase data augmentation
   --augment
   
   # Use pretrained weights
   --pretrained
   ```

---

**Ready to start training? Choose your model and follow the appropriate section above! 🚀**