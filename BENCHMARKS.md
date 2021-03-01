# Benchmarks
## Benchmark results of Arc, Flask, FastAPI, and Bottle using ApacheBench


### Arc
```py
from arc import App, TextResponse

app = App()

@app.route("/")
def index(request):
    return TextResponse("Test")

if __name__ == "__main__":
    app.run()
```

### Flask
```py
from flask import flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Test"

if __name__ == "__main__":
    app.run(debug=True)
```

### FastAPI
```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World"}
```

### Bottle
```py
from bottle import Bottle, run

app = Bottle()

@app.route('/')
def hello():
    return "Test"

run(app, host='localhost', port=8080)
```

Heres the benchmarking results with 5000 requests and a concurrency of 500.

### Arc (Default Server)
```
Concurrency Level:      500
Time taken for tests:   2.529 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      770000 bytes
HTML transferred:       10000 bytes
Requests per second:    1977.05 [#/sec] (mean)
Time per request:       252.902 [ms] (mean)
Time per request:       0.506 [ms] (mean, across all concurrent requests)
Transfer rate:          297.33 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   2.0      1       8
Processing:     9  246  28.4    249     321
Waiting:        1  175  47.2    180     254
Total:          9  248  27.3    251     321

Percentage of the requests served within a certain time (ms)
  50%    251
  66%    251
  75%    253
  80%    257
  90%    260
  95%    318
  98%    321
  99%    321
 100%    321 (longest request)
```

### FastAPI (Pure Uvicorn Server)
```
Concurrency Level:      500
Time taken for tests:   2.568 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      850000 bytes
HTML transferred:       130000 bytes
Requests per second:    1947.22 [#/sec] (mean)
Time per request:       256.776 [ms] (mean)
Time per request:       0.514 [ms] (mean, across all concurrent requests)
Transfer rate:          323.27 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.9      0       9
Processing:    10  252  22.6    255     287
Waiting:        1  178  41.5    179     266
Total:         10  253  21.4    255     287

Percentage of the requests served within a certain time (ms)
  50%    255
  66%    256
  75%    261
  80%    262
  90%    263
  95%    263
  98%    264
  99%    265
 100%    287 (longest request)
```
### Flask (Default Development Server)
```
Concurrency Level:      500
Time taken for tests:   7.799 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      770000 bytes
HTML transferred:       10000 bytes
Requests per second:    641.10 [#/sec] (mean)
Time per request:       779.905 [ms] (mean)
Time per request:       1.560 [ms] (mean, across all concurrent requests)
Transfer rate:          96.42 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   77 266.5      0    1027
Processing:     4  398 1172.4     92    6791
Waiting:        1  398 1172.4     92    6791
Total:          8  475 1420.8     92    7794

Percentage of the requests served within a certain time (ms)
  50%     92
  66%     95
  75%     96
  80%     97
  90%    102
  95%   4379
  98%   7710
  99%   7755
 100%   7794 (longest request)
```
### Bottle
The bottle test timed out, and only completed 4514 requests.

### Time for tests
- **Arc** -     2.529 seconds

- **FastAPI** - 2.568 seconds

- **Flask** -   7.799 seconds

- **Bottle** -  Didn't Finish

Alright, Flask fell behind the other two, and bottle didn't even complete the test, while Arc and FastAPI were pretty close together. Now, lets try running Flask and Bottle on a deployment server, and run Arc and FastAPI using Gunicorn with UvicornWorker. Below are the benchmarking results with 5000 requests with a concurrency of 500.

### Arc (Gunicorn with Uvicorn Worker)
```
Concurrency Level:      1000
Time taken for tests:   1.200 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      675000 bytes
HTML transferred:       10000 bytes
Requests per second:    4168.22 [#/sec] (mean)
Time per request:       239.911 [ms] (mean)
Time per request:       0.240 [ms] (mean, across all concurrent requests)
Transfer rate:          549.52 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   15  10.3     13      38
Processing:    28  212  39.8    217     276
Waiting:        1  193  36.8    205     249
Total:         28  228  40.0    236     289

Percentage of the requests served within a certain time (ms)
  50%    236
  66%    245
  75%    248
  80%    250
  90%    260
  95%    271
  98%    281
  99%    284
 100%    289 (longest request)

```
### FastAPI (Gunicorn with Uvicorn Worker)
```
Concurrency Level:      1000
Time taken for tests:   0.738 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      755000 bytes
HTML transferred:       130000 bytes
Requests per second:    6777.09 [#/sec] (mean)
Time per request:       147.556 [ms] (mean)
Time per request:       0.148 [ms] (mean, across all concurrent requests)
Transfer rate:          999.36 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    8   4.9      7      19
Processing:    20  131  29.5    130     195
Waiting:        1  114  29.2    105     168
Total:         20  139  30.8    135     214

Percentage of the requests served within a certain time (ms)
  50%    135
  66%    141
  75%    149
  80%    170
  90%    191
  95%    198
  98%    203
  99%    206
 100%    214 (longest request)
```
### Flask (Waitress Deployment Server)
```
Concurrency Level:      1000
Time taken for tests:   2.062 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      770000 bytes
HTML transferred:       10000 bytes
Requests per second:    2425.38 [#/sec] (mean)
Time per request:       412.307 [ms] (mean)
Time per request:       0.412 [ms] (mean, across all concurrent requests)
Transfer rate:          364.75 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   6.1      0      22
Processing:    10  368 101.6    411     430
Waiting:        1  368 101.6    411     430
Total:         22  371  95.8    411     431

Percentage of the requests served within a certain time (ms)
  50%    411
  66%    420
  75%    423
  80%    423
  90%    427
  95%    428
  98%    429
  99%    429
 100%    431 (longest request)
```
### Bottle (Waitress)
```
Concurrency Level:      1000
Time taken for tests:   1.679 seconds
Complete requests:      5000
Failed requests:        0
Non-2xx responses:      5000
Total transferred:      4405000 bytes
HTML transferred:       3600000 bytes
Requests per second:    2977.31 [#/sec] (mean)
Time per request:       335.873 [ms] (mean)
Time per request:       0.336 [ms] (mean, across all concurrent requests)
Transfer rate:          2561.54 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   5.1      0      18
Processing:    16  298  84.1    326     359
Waiting:        3  298  84.2    326     359
Total:         22  301  79.2    326     359

Percentage of the requests served within a certain time (ms)
  50%    326
  66%    334
  75%    345
  80%    348
  90%    356
  95%    357
  98%    357
  99%    357
 100%    359 (longest request)
```
### Time for tests
- **Arc** -     1.200 seconds

- **FastAPI** - 0.738 seconds

- **Flask** -    2.062 seconds

- **Bottle** -  1.679

Alright, from the above benchmarks, It's obvious that FastAPI is the most performant out of the four frameworks, and Arc comes in second place. In the first test, Bottle timed out, but in the second test, it pulled ahead of Flask, though not by much. If you perform your own benchmarks, I'd love it if you could send me the results. I'm doing the best I can to optimize Arc for better performance. If you're doing actual deployment with Arc, use gunicorn with uvicorn workers, as it yields the best results. Thanks for reading.