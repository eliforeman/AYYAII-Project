import magenta.music as mm
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel
from magenta.protobuf import music_pb2

# Initialize the model.
# print "Initializing Music VAE..."
music_vae = TrainedModel(
      configs.CONFIG_MAP['cat-mel_2bar_big'],
      batch_size=4,
      checkpoint_dir_or_path='./content/mel_2bar_big.ckpt')

# How many sequences, including the start and end ones, to generate.
num_steps = 4

twinkle_twinkle = music_pb2.NoteSequence()
twinkle_twinkle.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
twinkle_twinkle.notes.add(pitch=60, start_time=0.5, end_time=1.0, velocity=80)
twinkle_twinkle.notes.add(pitch=67, start_time=1.0, end_time=1.5, velocity=80)
twinkle_twinkle.notes.add(pitch=67, start_time=1.5, end_time=2.0, velocity=80)
twinkle_twinkle.notes.add(pitch=69, start_time=2.0, end_time=2.5, velocity=80)
twinkle_twinkle.notes.add(pitch=69, start_time=2.5, end_time=3.0, velocity=80)
twinkle_twinkle.notes.add(pitch=67, start_time=3.0, end_time=4.0, velocity=80)
twinkle_twinkle.notes.add(pitch=65, start_time=4.0, end_time=4.5, velocity=80)
twinkle_twinkle.notes.add(pitch=65, start_time=4.5, end_time=5.0, velocity=80)
twinkle_twinkle.notes.add(pitch=64, start_time=5.0, end_time=5.5, velocity=80)
twinkle_twinkle.notes.add(pitch=64, start_time=5.5, end_time=6.0, velocity=80)
twinkle_twinkle.notes.add(pitch=62, start_time=6.0, end_time=6.5, velocity=80)
twinkle_twinkle.notes.add(pitch=62, start_time=6.5, end_time=7.0, velocity=80)
twinkle_twinkle.notes.add(pitch=60, start_time=7.0, end_time=8.0, velocity=80)
twinkle_twinkle.total_time = 8
twinkle_twinkle.tempos.add(qpm=60)

babyshark = mm.midi_file_to_note_sequence('./mid/babyshark.mid')
babyshark = mm.extract_subsequence(babyshark, 0, 8)

babyshark.ticks_per_quarter = 0
babyshark.time_signatures.pop()
babyshark.key_signatures.pop()
babyshark.tempos.pop()
babyshark.tempos.add(qpm=60)


for note in babyshark.notes:
      if note.pitch < 60:
            note.pitch = 60
      note.instrument = 0
      note.is_drum = False

# This gives us a list of sequences.
note_sequences = music_vae.interpolate(
      twinkle_twinkle,
      babyshark,
      num_steps=num_steps,
      length=8)

# Concatenate them into one long sequence, with the start and
# end sequences at each end.
interp_seq = mm.sequences_lib.concatenate_sequences(note_sequences)

mm.play_sequence(interp_seq, synth=mm.fluidsynth)
mm.plot_sequence(interp_seq)

mm.sequence_proto_to_midi_file(interp_seq, 'twinkle_shark.mid')

