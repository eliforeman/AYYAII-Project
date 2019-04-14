# Import dependencies.
import magenta.music as mm
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel

# Initialize the model.
# print "Initializing Music VAE..."
music_vae = TrainedModel(
      configs.CONFIG_MAP['cat-mel_2bar_big'],
      batch_size=4,
      checkpoint_dir_or_path='./content/mel_2bar_big.ckpt')

# print ' Done!'

# Creating new sequences
# generated_sequences = music_vae.sample(n=2, length=80, temperature=1.0)

# for ns in generated_sequences:
#   # print(ns)
#   mm.plot_sequence(ns)
#   mm.play_sequence(ns, synth=mm.fluidsynth)

# We're going to interpolate between the Twinkle Twinkle Little Star
# NoteSequence we defined in the first section, and one of the generated
# sequences from the previous VAE example

# How many sequences, including the start and end ones, to generate.
num_steps = 8;

from test import twinkle_twinkle, teapot

# This gives us a list of sequences.
note_sequences = music_vae.interpolate(
      twinkle_twinkle,
      teapot,
      num_steps=num_steps,
      length=32)

# Concatenate them into one long sequence, with the start and
# end sequences at each end.
interp_seq = mm.sequences_lib.concatenate_sequences(note_sequences)

mm.play_sequence(interp_seq, synth=mm.fluidsynth)
mm.plot_sequence(interp_seq)

mm.sequence_proto_to_midi_file(interp_seq, 'vae_sample_output.mid')