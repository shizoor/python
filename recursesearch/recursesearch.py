#If you need to do a recursive search against a database with a REST API
#that returns JSON.  Search depth argument is for in case there's a circular reference
#Change baseurl as needed.  Python3
#usage : recursesearch.py IDENT DEPTH

import urllib, json
import urllib.request
import sys

baseurl = "http://192.168.0.23/public/readnames.php?id="




def teamlookup(ident, depth):
        if (depth>1):
                jsonurl = baseurl + str(ident)
                with urllib.request.urlopen(jsonurl) as url:
                        data = json.loads(url.read().decode())
                        print(ident, "  ", data['name'], "       ", data['children'])
                        #print(data['children'])
                        for x in data['children']:
                                teamlookup(x, (depth-1))

                return(data['children'])
        else:
                return('')


def main():
        ident = sys.argv[1]
        depth = sys.argv[2]

        teamlookup(int(ident), int(depth))

if __name__== '__main__':
        main()
