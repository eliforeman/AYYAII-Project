import magenta.music as mm
import magenta
import tensorflow

# print 'Downloading model bundle. This will take less than a minute...'
mm.notebook_utils.download_bundle('basic_rnn.mag', './content/')
bundle = mm.sequence_generator_bundle.read_bundle_file('./content/basic_rnn.mag')

# Import dependencies.
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

# Initialize the model.
# print "Initializing Melody RNN..."
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()

# print '🎉 Done!'

# Model options. Change these to get different generated sequences!
from test import twinkle_twinkle

input_sequence = twinkle_twinkle # change this to teapot if you want
num_steps = 128 # change this for shorter or longer sequences
temperature = 1.0 # the higher the temperature the more random the sequence.

# Set the start time to begin on the next step after the last note ends.
last_end_time = (max(n.end_time for n in input_sequence.notes)
                  if input_sequence.notes else 0)
qpm = input_sequence.tempos[0].qpm
seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
total_seconds = num_steps * seconds_per_step

generator_options = generator_pb2.GeneratorOptions()
generator_options.args['temperature'].float_value = temperature
generate_section = generator_options.generate_sections.add(
  start_time=last_end_time + seconds_per_step,
  end_time=total_seconds)

# Ask the model to continue the sequence.
sequence = melody_rnn.generate(input_sequence, generator_options)

mm.plot_sequence(sequence)
mm.play_sequence(sequence, synth=mm.fluidsynth)

mm.sequence_proto_to_midi_file(sequence, 'melody_sample_output.mid')