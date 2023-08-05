# mrequests
Using multiprocessing and requests to send requests using threads to fasten sending large number of requests.

## Usage
<pre>
from mrequests import MultiRequests
m = MultiRequests.PoolRequests(method='GET')
urls = ["https://www.google.com","https://www.yahoo.com"]
resp = m.send(urls)
for r in resp:
  print(r.status_code)
</pre>

## Installation
<pre>
pip3 install --index-url https://test.pypi.org/simple/ mrequests
</pre>


## Future Work
<ul>
  <li>Parameterized requests</li>
  <li>Authenticated Sessions</li>
 </ul>
