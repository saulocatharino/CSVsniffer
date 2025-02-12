import collections
import clevercsv
import time
import os

def getCSVdata(path: str)->str:
   with open(path) as f:
        csvcontent: str = ' '.join(f.readlines())
        return csvcontent

def DetectCSVDialect(path: str):
  try:
      content= getCSVdata(path)
      # you can use verbose=True to see what CleverCSV does
      dialect = clevercsv.Sniffer().sniff(content,delimiters=[',',';','\t','|',':','.','=','<','>',' '],verbose=True)
      return dialect
  except OSError as err:
    print("Error was: %s" % err)
  except Exception as err:
    print("Error was: %s" % err)

def ImportExpectedResults()->dict:
  try:
     with open(os.path.dirname(__file__) +'/DialectConf.txt', newline='') as csvfile:
        csvFilesDict={}
        csvRowDict={}
        spamreader = clevercsv.reader(csvfile, delimiter='|', quotechar='')
        i=0
        for row in spamreader:
           if len(row)>1:
              if i>0:
                 csvRowDict={
                    'encoding':row[1],
                    'fields_delimiter':row[2],
                    'quotechar':row[3],
                    'escapechar':row[4],
                    'records_delimiter':row[5]
                 }
                 csvFilesDict[row[0]]=csvRowDict
              else:
                 i+=1
        return csvFilesDict
  except Exception as err:
     print("Error was: %s" % err)

def GetDelName(aDelim:str)->str:
   if aDelim == ',':
      return 'comma'
   elif aDelim == ';':
      return 'semicolon'
   elif aDelim == '\t':
      return 'tab'
   elif aDelim == ' ':
      return 'space'
   elif aDelim == '|':
      return 'vslash'

def GetQuoteName(aQuote:str)->str:
   if aQuote == '"' or aQuote == '':
      return 'doublequote'
   elif aQuote == '\'':
      return 'singlequote'

#Import expectect results as nested dicts
ExpectedResults=ImportExpectedResults()
#Get test path withing current .py file
TestsCSVpath=os.path.dirname(__file__) + '/CSV/'
passed=0
failures=0
t=time.time()
#Iterate and run all test files
for filename in os.listdir(TestsCSVpath):
  file = os.path.join(TestsCSVpath, filename)
  #File check
  if os.path.isfile(file):
    try:
       dialect=DetectCSVDialect(file)
    except:
       dialect=None
    if dialect !=None:
      if GetDelName(dialect.delimiter)==ExpectedResults[filename]['fields_delimiter'] and \
        GetQuoteName(dialect.quotechar)==ExpectedResults[filename]['quotechar']:
         tflag ='+'
         passed += 1
      else:
         tflag ='X'
      if tflag =='+':
         print(tflag + '[' + filename + ']: --> cleverCSV detected: delimiter = %r, quotechar = %r' 
            % (dialect.delimiter, dialect.quotechar))
      else:
         print(tflag + '[' + filename + ']: --> cleverCSV detected: delimiter = %r, quotechar = %r' 
            % (dialect.delimiter, dialect.quotechar) + \
              '| EXPECTED:{delimiter = %r, quotechar = %r}' \
                % (ExpectedResults[filename]['fields_delimiter'], ExpectedResults[filename]['quotechar']))
    else:
      print("X [" + filename + "]: --> No result from cleverCSV")
      failures += 1
print('[Passed test ratio]--: %r' %(round(100*passed/len(ExpectedResults),4)) +'%')
print('[Failure ratio]--: %r' %(round(100*failures/len(ExpectedResults),4)) +'%')
print('[Elapsed time]--: %r seconds' %(round(time.time()-t,2)))