from pathlib import Path
BASE_DIR = Path('pybert')
config = {
    'raw_data_path': BASE_DIR / 'dataset/train_reply_deemoji.csv',
    'test_path': BASE_DIR / 'dataset/test_reply_deemoji.csv',

    'data_dir': BASE_DIR / 'dataset',
    'log_dir': BASE_DIR / 'output/log',
    'writer_dir': BASE_DIR / "output/TSboard",
    'figure_dir': BASE_DIR / "output/figure",
    'checkpoint_dir': BASE_DIR / "output/checkpoints",
    'cache_dir': BASE_DIR / 'model/',
    'result': BASE_DIR / "output/result",
}

