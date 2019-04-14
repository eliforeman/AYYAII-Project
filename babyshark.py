import magenta.music as mm

babyshark = mm.midi_file_to_note_sequence('./mid/babyshark_full.mid')

# truncate @ 14 seconds

truncated = mm.extract_subsequence(babyshark, 14, 14+8.5)

mm.sequence_proto_to_midi_file(truncated, './mid/babyshark.mid')


