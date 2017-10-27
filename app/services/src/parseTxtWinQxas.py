import re
import math
import pyxray

def checkLine(Z,energy):
    ok=None
    try:
        ok = pyxray.xray_transition_energy_eV(Z, 'La1')
    except:
        print("não tem")
    print(ok)

def parseTxtWinQxas(file_content):
    peaks = {}
    errors = {}

    lines = file_content.split("\n")
    
    Photopeakss_line = 4 # not sure if always...
    Photopeakss = int(lines[Photopeakss_line].split(',')[1].strip())

    for line in range(Photopeakss_line+1, Photopeakss_line + Photopeakss + 1):
        Z = int(lines[line].split(',')[0].strip())
        energy = float(lines[line].split(',')[1].strip())
        peak = int(lines[line].split(',')[2].strip())
        error = int(lines[line].split(',')[3].strip())
        
        peaks[Z] = peak
        errors[Z] = error
        checkLine(Z,energy)

    # Incoherent scattering peakss
    if lines[Photopeakss_line + Photopeakss + 1].startswith('Incoherent'):
            for line in range(Photopeakss_line + Photopeakss + 2, len(lines)):
                if len(lines[line].strip()) != 0: 
                    Z = int(lines[line].split(',')[0].strip())
                    peaks[Z] = peaks[Z] + int(lines[line].split(',')[2].strip())
                    Incoherent_errors = int(lines[line].split(',')[3].strip())
                    errors[Z] = math.sqrt(Incoherent_errors**2 + errors[Z]**2)

    return({'peaks': peaks, 'errors': errors})



