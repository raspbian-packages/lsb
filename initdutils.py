# Support for scanning init scripts for LSB info

import re, sys, os

FACILITIES = '/var/lib/lsb/facilities'

beginre = re.compile(re.escape('### BEGIN INIT INFO'))
endre = re.compile(re.escape('### END INIT INFO'))
linere = re.compile(r'\#\s+([^:]+):\s*(.*)')

def scan_initfile(initfile):
    headers = {'Description': []}
    scanning = 0
    
    for line in open(initfile).xreadlines():
        line = line.rstrip()
        if beginre.match(line):
            scanning = 1
            continue
        elif scanning and endre.match(line):
            scanning = 0
            continue
        elif not scanning:
            continue

        if line[0] != '#':
            continue

        if line[1:3] == '  ' or line[1] == '\t':
            headers['Description'].append(line[1:].strip())
            continue

        match = linere.match(line)
        if not match:
            print >> sys.stderr, "Warning: ignoring invalid init info line"
            print >> sys.stderr, "-> %s" % line
            continue

        header, body = match.groups()
        if header == "Description":
            headers[header].append(body.strip())
        elif header in ('Default-Start', 'Default-Stop'):
            headers[header] = map(int, body.split())
        elif header in ('Required-Start', 'Required-Stop', 'Provides'):
            headers[header] = body.split()
        else:
            headers[header] = body

    return headers

def save_facilities(facilities):
    if not facilities:
        try:
            os.unlink(FACILITIES)
        except OSError:
            pass
        return
    
    fh = open(FACILITIES, 'w')
    for facility, entries in facilities.items():
        if facility[0] == '$': continue
        for (scriptname, pri) in entries.items():
            start, stop = pri
            print >> fh, "%(scriptname)s %(facility)s %(start)d %(stop)d" % locals()
    fh.close()

def load_facilities():
    facilities = {}
    if os.path.exists(FACILITIES):
        for line in open(FACILITIES).xreadlines():
            try:
                scriptname, name, start, stop = line.strip().split()
                facilities.setdefault(name, {})[scriptname] = (int(start),
                                                               int(stop))
            except ValueError, x:
                print >> sys.stderr, 'Invalid facility line', line

    return facilities
