# RabbitMQ - Media Streaming Tests
This repo contains 3 producer-consumer pair of test scripts. Each producer emits out a frame of 720p@30fps, digested by the consumer and displayed to user. The 3 producer-consumer configrations are as follows: 

Results of these experiments are available <a href="https://docs.google.com/spreadsheets/d/1H4yaXyhLMSXv95ZCG8Gy7YiYUVs9MED7or3xUwP9l04/edit?usp=sharing">here</a>

![overview](https://user-images.githubusercontent.com/77619505/211662400-93faa900-3cb3-4ca9-aba2-49563c94bd46.png)


### Config 1 - No Encoding
The folder 'no-encoding' contains producer-consumer script pair where producer reads 720p frames, converts them to bytes and directs them to the consumer where they are converted back to a frame from byte string and then displayed.


### Config 2 - CPU Encoding
The folder 'cpu-encoding' contains producer-consumer script pair where producer reads 720p frames, <b>encodes them on CPU using OpenCV</b> and converts them to bytes and directs them to the consumer where they are converted back to a frame from byte string, <b>decoded</b> and then displayed.


### Config 3 - GPU Encoding
The folder 'gpu-encoding' contains producer-consumer script pair where producer reads 720p frames, <b>encodes them on GPU using nvJPEG</b> and directs them to the consumer where they are <b>decoded</b> and then displayed.




### To run a test
```
# Step 1 - Start rabbitmq container
./spinContainer.sh

# Step 2 - Start consumer process
cd cpu-encoding/
python 720-consumer-cpu-encoded.py

# Step 3 - Start producer process
720-consumer-cpu-encoded.py
```


### System Specs
| Hardware  | Spec |
| ------------- | ------------- |
| CPU  | 11th Gen Intel® Core™ i7-11800H @ 2.30GHz × 16  |
| GPU | GeForce RTX 3070 Mobile / Max-Q |
| RAM  | 16.0 GiB  |