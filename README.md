# SCC
Single-Cycle Chords

This program generates single-cycle waveforms for some just intonation chords with sines and bandlimited square and saw waves.

In equal temperament it is not possible to do this, because the ratios between the notes are irrational. In order to make short waveforms with more than one note that loop correctly (without clicks) you must use frequencies that are small ratios of each other, e.g. just intonation chords.

For example consider a chord with two sinewaves forming a 5th. In just intonation the ratio between the two frequencies is 2:3, this means that when the lowest frequency wave completes two cycles the highest frequency wave completes 3. In other words, 2 cycles of the lowest frequency wave contain 3 cycles of the highest frequency wave. And then it repeats periodically. In general, when the ratios between notes are rational (like happens with chords in just intonation), it makes sense to talk about single-cycle waveforms for the chords because the chords are actually periodic. In the SCWs built here I’m using the minimum period in order to make them as small as possible.

On the other hand, in equal temperament the waveforms of chords are not periodic, they never repeat, so it doesn’t really make sense to talk about single-cycle waveforms for chords in equal temperament.
