"""
This program creates single-cycle waveforms for just intonation chords.

2020/4/18, Luciano Notarfrancesco, github.com/len
"""

from math import pi, sin, cos, exp, log
import wave
import struct
import os

SAMPLE_RATE = 44100.0
F0 = 261.625565 # C3

chords = [
    ['unison', [1]],
    ['5th', [2,3]],
    ['4th', [3,4]],
    ['maj 3th', [4,5]],
    ['min 3th', [5,6]],
    ['maj', [4,5,6]],
#    ['maj', [1,3,5]], # spread-out
    ['min', [10,12,15]],
    ['dim', [5,6,7]], # perfect diminished
    ['dim', [20,24,29]],
    ['sus4', [6,8,9]],
    ['sus2', [8,9,12]],
    ['7', [4,5,6,7]], # harmonic 7
    ['9', [4,5,6,7,9]], # harmonic 9
    ['maj7', [4,5,6,18]],
    ['maj7', [8,10,12,15]],
    ['min7', [10,12,15,18]],
    ['min7b5', [5,6,7,9]], # half-diminished (perfect)
    ['dream', [12,16,17,18]],
    ['dom7', [20,25,30,36]],
    ['dom7b5', [25,30,36,45]],
    ['dom7#9', [20,25,30,36,48]],
#    ['dim7 17-limit', [10,12,14,17]], # Francois-Joseph Fetis (17-limit tuning)
    ['minmaj7', [40,48,60,75]]
]

def write_chord_sample_slice(wav, f0, ratios, func):
  f0 = SAMPLE_RATE / round(SAMPLE_RATE / f0) # round it for perfect loops!
  period = int(SAMPLE_RATE / f0)
  i = 0
  while i < period:
    t = i*pi*2/SAMPLE_RATE
    v = 0.0
    for r in ratios:
      f = f0 * r
      partials = int(SAMPLE_RATE/2/f) # Nyqist frequency / note frequency
      v += func(f*t, partials)
    v /= len(ratios)
    data = struct.pack('<h', int(32767*v))
    wav.writeframes(data)
    i += 1

def write_chord_sample(filename, f0, ratios, func):
  wav = wave.open(filename+'.wav','w')
  wav.setnchannels(1)
  wav.setsampwidth(2)
  wav.setframerate(SAMPLE_RATE)
  print(filename)
  write_chord_sample_slice(wav, f0, ratios, func)
  wav.close()

def ratios_string(ratios):
  answer = ''
  first = True
  for r in ratios:
    if first:
      first = False
      if r < 10: answer += ' ' # pad with space so chords with small ratios show up first when browsing samples in octatrack
      answer += '%d' % r
    else:
      answer += ',%d' % r
  if len(ratios) == 1 and ratios[0] == 1:
    answer += ',1' # special notation for unison
  return answer

def ensure_path_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)

def write_all_chords(func, path):
  ensure_path_exists(path)
  for chord in chords:
    name = chord[0]
    ratios = chord[1]
    filename = path+'/'+ratios_string(ratios)+' '+name
    write_chord_sample(filename, F0 / ratios[0], ratios, func) # root position, root at 0
    for position in range(1,len(ratios)):
      inversion = list(map(lambda ratio: ratio*2, ratios[:position]))+ratios[position:]
      inversionPath = path+'/'+['1st','2nd','3rd','4th'][position-1]+' inversion'
      ensure_path_exists(inversionPath)
      filename = inversionPath+'/'+ratios_string(ratios)+'-'+str(position)+' '+name
      write_chord_sample(filename, F0 / ratios[0], inversion, func)

def osc_sine(x, partials):
  return sin(x)

def osc_saw(x, partials):
  k = pi/2/partials
  v = 0.0
  for n in range(1,partials):
    m = cos((n-1)*k)
    m *= m
    v += sin(n*x)/n * m # reduce amplitude of higher partials to minimize Gibbs effect
  v = v / 2
  return v

def osc_square(x, partials):
  k = pi/2/partials
  v = 0.0
  for n in range(1,partials):
    if n%2==0: continue
    m = cos((n-1)*k)
    m *= m
    v += sin(n*x)/n * m # reduce amplitude of higher partials to minimize Gibbs effect
  return v

write_all_chords(osc_saw, 'saw')
write_all_chords(osc_sine, 'sine')
write_all_chords(osc_square, 'square')

