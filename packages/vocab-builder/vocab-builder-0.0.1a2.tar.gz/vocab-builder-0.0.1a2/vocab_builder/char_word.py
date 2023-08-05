from .char import CharVocab


class CharWordVocab(CharVocab):
    def to_seq(self, sentence: str, seq_len: int = None,
               char_seq_len=10, word_seq_len=10, mid_pad=True,
               with_eos=False, with_sos=False, with_len=False):
        seq = [
            super(CharWordVocab, self).to_seq(token, seq_len=char_seq_len, mid_pad=mid_pad)
            for token in sentence.split()
        ]

        if with_eos:
            seq += [self.eos_index]  # this would be index 1
        if with_sos:
            seq = [self.sos_index] + seq

        origin_seq_len = len(seq)

        if seq_len is None:
            pass
        elif len(seq) <= seq_len:
            seq += [[self.pad_index for _ in range(char_seq_len)]
                    for _ in range(seq_len - len(seq))]
        else:
            seq = seq[:seq_len]

        return (seq, origin_seq_len) if with_len else seq

    def from_seq(self, seq, join=False, with_pad=False):
        tokens = [super(CharWordVocab, self).from_seq(token, join=True, with_pad=False)
                  for token in seq]
        return " ".join(tokens) if join else tokens
