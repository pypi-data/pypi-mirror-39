import re
import urllib.request

str = '''
"we need to inform him with the latest information"
'''

s1 = re.findall("inform", str)
print(s1)

str = "sat, mat, hat, pat"

s1 = re.findall("[shmp]at",str)

print(s1)

s1 = re.findall("[h-m]at",str)

print(s1)





# Validate a phone number of pattern XXX-XXX-XXXX

phnum = "333-111-1234"

if re.search("\d{3}-\d{3}-\d{4}", phnum):
    print("This is a valid phone number")
else:
    print("It isnt a phone number")


# web scrape the phone numbers from a website

url = "http://www.summet.com/dmsi/html/codesamples/addresses.html"
response = urllib.request.urlopen(url)
html = response.read()
htmlStr = html.decode()

pdData = re.findall("\(\d{3}\) \d{3}-\d{4}", htmlStr)

for item in pdData:
    print(item)