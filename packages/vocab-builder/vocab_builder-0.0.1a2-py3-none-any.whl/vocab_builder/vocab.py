import pickle

from collections import Counter
from .base import TorchVocab


class Vocab(TorchVocab):
    def __init__(self, texts, max_size=None, min_freq=1):
        self.pad_index = 0
        self.unk_index = 1
        self.eos_index = 2
        self.sos_index = 3
        self.mask_index = 4

        print("Building Vocab")
        counter = Counter()
        for text in texts:
            tokens = self.tokenizer(text)
            for token in tokens:
                counter[token] += 1

        super().__init__(counter, specials=["<pad>", "<unk>", "<eos>", "<sos>", "<mask>"],
                         max_size=max_size, min_freq=min_freq)

    def to_seq(self, sentence: str, seq_len: int = None, with_eos=False, with_sos=False, with_len=False,
               mid_pad=False) -> list:
        tokens = self.tokenizer(sentence)
        seq = [self.stoi.get(c, self.unk_index) for c in tokens]

        if with_eos:
            seq += [self.eos_index]  # this would be index 1
        if with_sos:
            seq = [self.sos_index] + seq

        origin_seq_len = len(seq)

        if seq_len is None:
            pass
        elif len(seq) <= seq_len:
            if not mid_pad:
                seq += [self.pad_index for _ in range(seq_len - len(seq))]
            else:
                front_pad = [self.pad_index for _ in range(int((seq_len - len(seq)) / 2))]
                end_path = [self.pad_index for _ in range(seq_len - len(seq) - len(front_pad))]
                seq = front_pad + seq + end_path
        else:
            seq = seq[:seq_len]

        return (seq, origin_seq_len) if with_len else seq

    def from_seq(self, seq, join=False, with_pad=False):
        tokens = [self.itos[idx]
                  if idx < len(self.itos)
                  else "<%d>" % idx
                  for idx in seq
                  if with_pad or idx != self.pad_index]

        return self.joiner(tokens) if join else tokens

    def tokenizer(self, sentence: str) -> list:
        return sentence.strip().split()

    def joiner(self, tokens: list) -> str:
        return " ".join(tokens)

    @staticmethod
    def load_vocab(vocab_path: str):
        with open(vocab_path, "rb") as f:
            return pickle.load(f)

    def save_vocab(self, vocab_path):
        with open(vocab_path, "wb") as f:
            pickle.dump(self, f)
