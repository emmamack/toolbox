"""Synthesizes a blues solo algorithmically."""

import atexit
import os
from random import choice

from psonic import *


# The sample directory is relative to this source file's directory.
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

SAMPLE_FILE = os.path.join(SAMPLES_DIR, "bass_D2.wav")
SAMPLE_NOTE = D2  # the sample file plays at this pitch

def play_note(note, beats=1, bpm=60, amp=1):
    """Play note for `beats` beats. Return when done."""
    # `note` is this many half-steps higher than the sampled note
    half_steps = note - SAMPLE_NOTE
    # An octave higher is twice the frequency. There are twelve half-steps per
    # octave. Ergo, each half step is a twelth root of 2 (in equal temperament).
    rate = (2 ** (1 / 12)) ** half_steps
    assert os.path.exists(SAMPLE_FILE)
    # Turn sample into an absolute path, since Sonic Pi is executing from a
    # different working directory.
    sample(os.path.realpath(SAMPLE_FILE), rate=rate, amp=amp)
    sleep(beats * 60 / bpm)


def stop():
    """Stop all tracks."""
    msg = osc_message_builder.OscMessageBuilder(address='/stop-all-jobs')
    msg.add_arg('SONIC_PI_PYTHON')
    msg = msg.build()
    synth_server.client.send(msg)


# stop all tracks when the program exits normally or is interrupted
atexit.register(stop)

BLUES_SCALE = [
    40, 43, 45, 46, 47, 50, 52, 55, 57, 58, 59, 62, 64, 67, 69, 70, 71, 74, 76]



# set variables
BEATS_PER_MINUTE = 90
SWING_AMT = .7      #integer from 0 to 1, 0 is maximum, 1 minimum
num_licks = 8


swing_lengths = [2 - SWING_AMT, SWING_AMT]
starters = [0,6,12,18]
swing_ind = 0
curr_note = 0
licks = [[(0, 0.5), (1, 0.5), (1, 0.5), (1, 0.5)],[(1, 0.5), (2, 0.5), (1, 0.5), (-1, 0.5)],
        [(4, 0.5), (-1, 0.5), (-1, 0.5), (-1, 0.5)],[(-3, 0.5), (1, 0.5), (-3, 0.5), (1, 0.5)]]
for _ in range(num_licks):
    lick = random.choice(licks)
    curr_note = random.choice(starters)
    if _ == num_licks -1:
        curr_note = 0
        lick = licks[0]
    for note in lick:
        curr_note += note[0]
        if curr_note > len(BLUES_SCALE) - 1:
            curr_note -= 6
        if curr_note < 0:
            curr_note += 6
        play_note(BLUES_SCALE[curr_note], note[1] * swing_lengths[swing_ind], BEATS_PER_MINUTE)
        swing_ind = abs(swing_ind -1)
play_note(BLUES_SCALE[0], 1 * swing_lengths[swing_ind], BEATS_PER_MINUTE)
