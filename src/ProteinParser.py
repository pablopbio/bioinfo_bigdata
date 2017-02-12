import re
import sys
import os

class ProteinParser(object) :

    # We set the file handler inside the object to access it everywhere.
    # fieldsToParse list is used to not repeat parsing a element once it has been parsed.
    # fieldsRegExp corresponds to the ones to match the field

    def __init__(self, fileHandler):
        self.fileHandler = fileHandler
        self.attributeGeneral = '^\s{0,2}[A-Z]+\s [A-Z]*'
        self.fieldsToParse = ["id", "name"]#, "org", "links", "seq"]
        self.fieldsRegExp = {"id"   : "LOCUS\s*(.*)",
                             "name" : "DEFINITION\s*(.*)"}

    def __iter__(self):
        return self

    def getId(self, matches):
        result = matches.group(1)
        return result.split()[0]

    def getName(self, matches):
        result = re.search("(hypothetical protein)? (.*)(\, partial)? \[.*\].", matches.group(1))
        if result is not None:
            return result.group(2)


    def next(self):
        valuesDict = {'id':'not available', 'name':'not available'}#, 'org':'not available', 'links':'not available',
                      #'seq':'not available'}

        isGeneraltt = False
        readingValue = True
        valueGotten = False
        value = ""
        for line in self.fileHandler:
            line = line.rstrip('\n')
            if re.search('^//', line) is not None:
                return valuesDict
            # check if we are at the star line of a new attribute
            regAtExp = re.compile(self.attributeGeneral)
            isGeneraltt = regAtExp.match(line)
            if isGeneraltt:
                if readingValue:
                    value = line
                    valueGotten = True
                    value.rstrip('\n')
                    for field in self.fieldsToParse:
                        matches = re.search(self.fieldsRegExp[field], value)
                        if matches is not None:
                            if field == "id":
                                valuesDict[field] = self.getId(matches)
                            elif field == "name":
                                valuesDict[field] = self.getName(matches)
            else:
                value += line

        raise StopIteration



def checkParams():
    if len(sys.argv) == 4:
        if not os.path.isfile(sys.argv[1]):
            raise OSError

#        if os.path.isfile(sys.argv[2]):
#            print "aqui"
#            opt = raw_input('Output file ', sys.argv[2], ' exists, do you want to overwrite? (y/n)')
#            print opt
#            if opt != "y":
#                raise RuntimeError
#
#       if os.path.isfile(sys.argv[3]):
#          if raw_input('Output file ', sys.argv[3], ' exists, do you want to overwrite? (y/n)') != "y":
#                raise RuntimeError
#
        return True
    else:
        raise StandardError


if __name__ == '__main__':

    try :
        checkParams()
    except OSError:
        print 'File ', sys.argv[1], ' doesn\'t exists'
        exit()

    except RuntimeError:
        print 'Operation cancelled by user...'

    except StandardError:
        print ('Usage: python ProteinParser origin_file output_tab_file output_FASTA_file')

    fHandler = open(sys.argv[1], 'r')
    valuesDict = {'id':'not available'}#, 'name':'not available', 'org':'not available', 'links':'not available',
              #    'seq':'not available'}
    for valuesDict in ProteinParser(fHandler):
        print "id: ", valuesDict['id']
        print "gene name: ", valuesDict['name']


