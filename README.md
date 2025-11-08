# home-made-scheduler

## how to use
```
cd learn
cmake .
make -j
```
and run `./server` and in different terminal run `./client <TPU-monster>`

expected server output:
Server running on 0.0.0.0:50051
[worker] Background worker started
[server] Enqueued task for: TPU-monster
[server] Waiting for worker to process: TPU-monster
[worker] Processing task for: TPU-monster
worker task took 0.02 ms
[worker] Finished processing: TPU-monster
end-to-end RPC took 0.11 ms
[server] Response sent for: TPU-monster

expected client output:
Hello, TPU-monster!

## why am i making this
I realized cpp/application is much more than what I've explored so far and I want to get into it as soon as I can. Here I've tried to learn to
1. set up gRPC + how to structure a proto file
2. properly make a CMake file
3. build my own thread - a "worker" or mini scheduler
4. use mutex and conditional variable so worker waits until job arrives
5. add a scoped timer (RAII) 

## more soon?
I think I could implement round robin much better than how I have previously if I use these, probably task for tomorrow.
I would really like to visualize/graph performance timings. I want to put all timings in a csv and graph them.
gRPC streaming API? inference runtime experiment? 

