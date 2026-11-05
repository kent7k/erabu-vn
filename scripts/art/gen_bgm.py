#!/usr/bin/env python3
"""BGM 2 曲を numpy で合成する（P3・自作）。素材もサンプルも使わないので権利の問題は無い。

  python3 scripts/art/gen_bgm.py --out <dir>      # bgm_day.wav / bgm_night.wav

末尾の余韻は先頭へ巻き戻して足す（円環の畳み込み）ので、ループの継ぎ目で音が切れない。
"""
import argparse, wave
from pathlib import Path

import numpy as np

SR = 44100
NAMES = {"C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "Gb": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}


def midi(n):
    return 12 * (int(n[-1]) + 1) + NAMES[n[:-1]]


def felt_piano(pitch, dur, vel, seed):
    """フェルトを噛ませたピアノに寄せた加算合成。高い倍音ほど早く減衰する。"""
    f0 = 440.0 * 2 ** ((pitch - 69) / 12)
    n = int(SR * (dur + 2.6))
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    out = np.zeros(n)
    for k in range(1, 13):
        fk = f0 * k * np.sqrt(1 + 0.00035 * k * k)
        if fk > SR * 0.42:
            break
        amp = (vel ** (0.6 + k * 0.16)) / k ** 1.7
        dec = 0.75 + 0.42 * k + f0 / 900
        det = 1 + rng.normal(0, 0.00025)
        out += amp * np.exp(-t * dec) * np.sin(2 * np.pi * fk * det * t + rng.uniform(0, 6.28))
    atk = np.minimum(t / 0.012, 1.0)
    rel = np.clip((dur + 1.1 - t) / 1.1, 0, 1) ** 2
    return out * atk * rel * vel


def pad(pitches, dur, level):
    n = int(SR * dur)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for p in pitches:
        f = 440.0 * 2 ** ((p - 69) / 12)
        out += np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.003 * t) + 0.5 * np.sin(2 * np.pi * f * 0.998 * t)
    env = np.minimum(t / (dur * 0.35), 1) * np.minimum((dur - t) / (dur * 0.35), 1)
    return out * env * level


def add(buf, sig, start, pan):
    """円環のバッファへ足す（はみ出した余韻は先頭へ戻る）。"""
    L = buf.shape[1]
    idx = (start + np.arange(len(sig))) % L
    np.add.at(buf[0], idx, sig * np.cos(pan * np.pi / 2))
    np.add.at(buf[1], idx, sig * np.sin(pan * np.pi / 2))


def reverb(buf, seconds, wet, seed):
    """指数減衰のノイズを残響に使う。FFT の円環畳み込みなのでループの継ぎ目が無い。"""
    L = buf.shape[1]
    t = np.arange(int(SR * seconds)) / SR
    out = np.zeros_like(buf)
    for ch in range(2):
        rng = np.random.default_rng(seed + ch)
        ir = rng.normal(0, 1, len(t)) * np.exp(-t * 6.9 / seconds)
        kernel = np.ones(14) / 14
        ir = np.convolve(ir, kernel, mode="same")
        ir[:int(SR * 0.012)] = 0
        pad_ir = np.zeros(L)
        pad_ir[:len(ir)] = ir
        conv = np.fft.irfft(np.fft.rfft(buf[ch]) * np.fft.rfft(pad_ir), L)
        conv *= np.sqrt((buf[ch] ** 2).mean() / max((conv ** 2).mean(), 1e-12))
        out[ch] = buf[ch] * (1 - wet) + conv * wet
    return out


def render(bpm, bars, chords, melody, arp, seed, vel_arp, vel_mel, pad_level, rv_sec, rv_wet):
    beat = 60 / bpm
    L = int(SR * beat * 4 * bars)
    buf = np.zeros((2, L))
    rng = np.random.default_rng(seed)
    for b, chord in enumerate(chords):
        ps = [midi(x) for x in chord]
        add(buf, pad(ps[1:4], beat * 4.6, pad_level), int(SR * beat * 4 * b), 0.5)
        for i, (pos, idx) in enumerate(arp):
            p = ps[idx % len(ps)]
            start = int(SR * beat * (4 * b + pos + rng.normal(0, 0.006)))
            v = vel_arp * rng.uniform(0.86, 1.0) * (1.0 if idx == 0 else 0.86)
            add(buf, felt_piano(p, beat * 1.5, v, seed + b * 97 + i), start % L, 0.32 + 0.36 * (p - 36) / 48)
    for j, (bar, pos, name, durb) in enumerate(melody):
        p = midi(name)
        start = int(SR * beat * (4 * (bar - 1) + (pos - 1) + rng.normal(0, 0.008)))
        add(buf, felt_piano(p, beat * durb, vel_mel * rng.uniform(0.88, 1.0), seed + 5000 + j), start % L, 0.58)
    out = reverb(buf, rv_sec, rv_wet, seed)
    out /= np.abs(out).max() / 0.7
    return np.tanh(out * 1.05)


DAY = dict(
    bpm=76, bars=16, seed=11, vel_arp=0.40, vel_mel=0.62, pad_level=0.007, rv_sec=2.2, rv_wet=0.22,
    arp=[(0, 0), (1, 1), (1.5, 2), (2, 3), (3, 2), (3.5, 1)],
    chords=[["F2", "C3", "A3", "C4"], ["E2", "C3", "G3", "C4"], ["D2", "A2", "F3", "C4"], ["Bb1", "F2", "D3", "A3"],
            ["A1", "F2", "C3", "A3"], ["Bb1", "F2", "D3", "F3"], ["G1", "D2", "Bb2", "F3"], ["C2", "G2", "Bb2", "F3"],
            ["D2", "A2", "F3", "A3"], ["A1", "E2", "C3", "G3"], ["Bb1", "F2", "D3", "A3"], ["A1", "F2", "C3", "A3"],
            ["G1", "D2", "Bb2", "F3"], ["C2", "G2", "C3", "E3"], ["Bb1", "F2", "D3", "A3"], ["C2", "G2", "C3", "F3"]],
    melody=[(1, 1, "A4", 2), (1, 3.5, "C5", 1.5), (2, 1, "G4", 2), (2, 3, "E4", 2), (3, 1, "F4", 1), (3, 2, "A4", 1.5), (3, 3.5, "C5", 1.5),
            (4, 1, "D5", 2), (4, 3, "C5", 2), (5, 1, "C5", 1.5), (5, 2.5, "A4", 1.5), (5, 4, "G4", 1), (6, 1, "F4", 3), (7, 1, "G4", 1.5), (7, 2.5, "Bb4", 1.5), (7, 4, "A4", 1),
            (8, 1, "G4", 3), (9, 1, "A4", 1.5), (9, 2.5, "D5", 2.5), (10, 1, "C5", 1.5), (10, 2.5, "A4", 1.5), (10, 4, "G4", 1), (11, 1, "F4", 1), (11, 2, "A4", 1), (11, 3, "D5", 2),
            (12, 1, "C5", 3), (13, 1, "Bb4", 1.5), (13, 2.5, "A4", 1.5), (13, 4, "G4", 1), (14, 1, "E4", 1.5), (14, 2.5, "G4", 2.5), (15, 1, "F4", 2), (15, 3, "A4", 2), (16, 1, "G4", 4)],
)
NIGHT = dict(
    bpm=54, bars=16, seed=23, vel_arp=0.30, vel_mel=0.46, pad_level=0.012, rv_sec=3.4, rv_wet=0.34,
    arp=[(0, 0), (1, 1), (2, 2), (3, 3)],
    chords=[["D2", "A2", "F3", "E4"], ["Bb1", "F2", "D3", "A3"], ["G1", "D2", "Bb2", "A3"], ["A1", "E2", "D3", "G3"],
            ["D2", "A2", "F3", "E4"], ["F2", "C3", "A3", "E4"], ["G1", "D2", "Bb2", "F3"], ["A1", "E2", "D3", "G3"],
            ["Bb1", "F2", "D3", "A3"], ["A1", "F2", "C3", "E4"], ["G1", "D2", "Bb2", "F3"], ["D2", "A2", "F3", "C4"],
            ["Bb1", "F2", "D3", "F3"], ["C2", "G2", "E3", "G3"], ["A1", "E2", "D3", "G3"], ["A1", "E2", "C#3".replace("C#", "Db"), "G3"]],
    melody=[(1, 3, "A4", 2), (2, 2, "F4", 3), (3, 3, "D4", 2), (4, 1, "E4", 4), (5, 3, "A4", 2), (6, 1, "C5", 3), (7, 2, "Bb4", 3), (8, 1, "A4", 4),
            (9, 3, "D5", 2), (10, 1, "C5", 3), (11, 2, "Bb4", 2), (11, 4, "A4", 1), (12, 1, "F4", 4), (13, 3, "D4", 2), (14, 1, "E4", 2), (14, 3, "G4", 2), (15, 1, "A4", 4)],
)


def write(path, st):
    pcm = (np.clip(st.T, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    rms = 20 * np.log10(np.sqrt((st ** 2).mean()))
    print(Path(path).name, f"{st.shape[1] / SR:.1f}s peak={np.abs(st).max():.2f} rms={rms:.1f}dB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True)
    out = Path(ap.parse_args().out); out.mkdir(parents=True, exist_ok=True)
    write(out / "bgm_day.wav", render(**DAY))
    write(out / "bgm_night.wav", render(**NIGHT))
