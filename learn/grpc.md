### Test using grpcurl
```bash
grpcurl -plaintext -proto inference.proto -d '{"name": "YourName"}' localhost:50051 demo.Greeter/SayHello
```

- -plaintext: don't use encryption (server only accepts unencrypted connections)
- -proto inference.proto: proto file location
- demo.Greeter/SayHello: function to call (defined in proto file)

### Step 2, build your own client

using: CreateChannel, NewStub, ClientContext, stub->function - call rpc, check status

### Step 3, add a worker

using: thread, mutex, condition_variable, queue, promise+future



