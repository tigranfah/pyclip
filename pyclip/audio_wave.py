import librosa


class AudioWaveInfo:

    def __init__(self, audio_ts):
        self.wave_length = len(audio_ts)
        self._wave_indices = (0, self.wave_length)
        self.pos_in_movie = ()

    @property
    def wave_indices(self):
        return self._wave_indices

    @wave_indices.setter
    def wave_indices(self, ind):
        self.wave_length = ind[1] - ind[0]
        self._wave_indices = ind


class AudioWave:

    def __init__(self, path):
        self._audio_ts, self._sampling_rate = librosa.load(path)
        self.info = AudioWaveInfo(self._audio_ts)

    @property
    def audio_ts(self):
        return self._audio_ts

    @property
    def sampling_rate(self):
        return self._sampling_rate
