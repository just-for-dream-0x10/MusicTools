# MusicAITools - 音乐AI处理工具包

MusicAITools 是一个多功能音乐处理工具包，提供音频文件处理、音乐文件格式转换和音乐分析等功能。

## 功能特点

- **音频格式转换**: 支持WAV, MP3, OGG, FLAC等格式的互相转换
- **音频转MIDI**: 将音频文件自动转换为MIDI格式
- **MIDI和MusicXML互转**: 支持MIDI和MusicXML（乐谱格式）之间的转换
- **MusicXML分析**: 分析乐谱的调性、音符统计和节奏分布
- **乐器转换**: 修改MusicXML文件中的乐器设置
- **音频分离**: 分离混合音频为人声、鼓点、贝斯和其他乐器
- **音频可视化**: 生成音频波形图、频谱图、梅尔频谱图、色度图等多种分析图表，支持多彩色彩方案
- **音频增强**: 提升旧录音或低质量音频的音质

未来计划： 加入完整的乐器音色提取功能，以及音频修复功能

## 安装

1. 克隆仓库:
```bash
git clone https://github.com/yourusername/MusicAITools.git
cd MusicAITools
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行界面

```bash
python main.py <命令> [选项]
```

可用命令:

1. **音频格式转换**:
```bash
python main.py convert-format input.wav -f mp3 -o output.mp3
```

2. **音频转MIDI**:
```bash
python main.py audio-to-midi input.wav -o output.mid
```

3. **MIDI转MusicXML**:
```bash
python main.py midi-to-xml input.mid -o output.musicxml
```

4. **MusicXML转MIDI**:
```bash
python main.py xml-to-midi input.musicxml -o output.mid
```

5. **分析MusicXML**:
```bash
python main.py analyze score.musicxml
```

6. **更改乐器**:
```bash
python main.py change-instrument score.musicxml "Piano" -o new_score.musicxml
```

7. **音频分离**:
```bash
python main.py separate song.mp3 --output-dir separated_tracks
```

8. **音频可视化**:
```bash
python main.py visualize input.wav --output-file visualization.png
```

9. **音频修复**:
```bash
python main.py restore old_recording.wav -o restored.wav --noise-reduction 0.3 --eq-high 1.3
```

## 项目结构

```
MusicAITools/
│
├── main.py               # 主程序入口和CLI界面
├── requirements.txt      # 项目依赖
│
├── modules/              # 功能模块
│   ├── conversion/       # 格式转换相关模块
│   │   ├── audio_to_midi.py
│   │   ├── midi_to_musicxml.py
│   │   ├── musicxml_to_midi.py
│   │   └── format_converter.py
│   │
│   ├── analysis/         # 音乐分析相关模块
│   │   └── musicxml_analyzer.py
│   │
│   ├── audio/            # 音频处理相关模块
│   │   ├── separator.py
│   │   ├── visualizer.py
│   │   └── restoration.py
│   │
│   └── utils/            # 工具函数
│       └── helpers.py
│
└── tests/                # 测试代码
```

## 许可证

MIT License

---