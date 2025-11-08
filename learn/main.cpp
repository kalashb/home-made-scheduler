#include <grpcpp/grpcpp.h>

#include <iostream>

#include "inference.grpc.pb.h"

using demo::Greeter;
using demo::HelloReply;
using demo::HelloRequest;
using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

// server-side implementation
class GreeterServiceImpl final : public Greeter::Service {
 public:
  Status SayHello(ServerContext*, const HelloRequest* req,
                  HelloReply* rep) override {
    rep->set_message("Hello, " + req->name() + "!");
    std::cout << "Greeted " << req->name() << std::endl;
    return Status::OK;
  }
};

int main() {
  GreeterServiceImpl service;

  ServerBuilder builder;
  builder.AddListeningPort("0.0.0.0:50051", grpc::InsecureServerCredentials());
  builder.RegisterService(&service);

  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server running on port 50051\n";
  server->Wait();
}