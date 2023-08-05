import csv
from ..pitch import Pitch

def pitches_to_csv(filename, pitches):
    """
    Convert Pitch instances to a csv file.
    
    Params
    ------
    filename : string
      csv file
    pitches : Pitch instance
      pitches
    """
    csvfile = open(filename, "w")
    writer = csv.DictWriter(csvfile, sorted(Pitch.PITCH_ATTRS))
    writer.writeheader()
    for pitch in pitches:
        pitch_row_copy = { k:pitch.__dict__[k] for k in Pitch.PITCH_ATTRS }
        writer.writerow(pitch_row_copy)
    csvfile.close()
                
