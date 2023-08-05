import pickle
import tqdm

from collections import Counter
from .vocab import Vocab


# Building Vocab with text files
class CharVocab(Vocab):
    def __init__(self, texts, max_size=None, min_freq=1):
        print("Building Vocab")
        counter = Counter()
        for line in tqdm.tqdm(texts):
            if isinstance(line, str):
                line = line.strip()

            for c in line:
                counter[c] += 1
        super().__init__(counter, max_size=max_size, min_freq=min_freq)

    def to_seq(self, sentence: str, seq_len=None, with_eos=False, with_sos=False, with_len=False):
        seq = [self.stoi.get(c, self.unk_index) for c in sentence]

        if with_eos:
            seq += [self.eos_index]  # this would be index 1
        if with_sos:
            seq = [self.sos_index] + seq

        origin_seq_len = len(seq)

        if seq_len is None:
            pass
        elif len(seq) <= seq_len:
            seq += [self.pad_index for _ in range(seq_len - len(seq))]
        else:
            seq = seq[:seq_len]

        return (seq, origin_seq_len) if with_len else seq

    def from_seq(self, seq: list, join=False, with_pad=False):
        characters = [self.itos[idx]
                      if idx < len(self.itos)
                      else "<%d>" % idx
                      for idx in seq
                      if not with_pad or idx != self.pad_index]

        return "".join(characters) if join else characters

    @staticmethod
    def load_vocab(vocab_path: str) -> 'CharVocab':
        with open(vocab_path, "rb") as f:
            return pickle.load(f)
