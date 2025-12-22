from .audio_io import load_audio, save_audio, normalize_audio
from .effects import hard_clip, soft_clip
from .analysis import plot_time_domain, plot_frequency_domain, plot_comparison
from .processor import AudioProcessor

__all__ = [
    'load_audio',
    'save_audio',
    'normalize_audio',
    'hard_clip',
    'soft_clip',
    'plot_time_domain',
    'plot_frequency_domain',
    'plot_comparison',
    'AudioProcessor'
]
