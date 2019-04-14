import magenta.music as mm

babyshark = mm.midi_file_to_note_sequence('./mid/babyshark_full.mid')

# truncate @ 14 seconds

babyshark = mm.extract_subsequence(babyshark, 14, 14+8.5)
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

mm.sequence_proto_to_midi_file(babyshark, './mid/babyshark.mid')


