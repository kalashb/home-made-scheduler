#include <grpcpp/grpcpp.h>

#include <iostream>
#include <string>

#include "inference.grpc.pb.h"

int main(int argc, char** argv) {
  std::string name = (argc > 1) ? argv[1] : "World";

  auto channel = grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()); // insecure connection
  std::unique_ptr<demo::Greeter::Stub> stub = demo::Greeter::NewStub(channel);

  demo::HelloRequest req;
  req.set_name(name);

  demo::HelloReply rep;
  grpc::ClientContext ctx;

  grpc::Status status = stub->SayHello(&ctx, req, &rep);
  if (!status.ok()) {
    std::cerr << "RPC failed: " << status.error_message() << "\n";
    return 1;
  }

  std::cout << rep.message() << "\n";
  return 0;
}
