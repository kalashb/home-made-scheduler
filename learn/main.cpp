#include <grpcpp/grpcpp.h>

#include <chrono>
#include <condition_variable>
#include <fstream>
#include <functional>
#include <future>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>

#include "inference.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

// CSV logging helper
namespace {
std::mutex csv_mutex_;
bool csv_header_written_ = false;

void writeToCSV(const std::string& label, double ms) {
  std::lock_guard<std::mutex> lock(csv_mutex_);
  std::ofstream file("timings.csv", std::ios::out | std::ios::app);
  if (file.is_open()) {
    if (!csv_header_written_) {
      file << "label,time_ms\n";
      csv_header_written_ = true;
      std::cout << "[CSV] Created timings.csv\n";
    }
    file << label << "," << ms << "\n";
    file.close();
  } else {
    std::cerr << "[CSV] ERROR: Failed to open timings.csv\n";
  }
}
}  // namespace

struct ScopedTimer {
  std::string label;
  std::chrono::high_resolution_clock::time_point t0;

  explicit ScopedTimer(std::string l)
      : label(std::move(l)), t0(std::chrono::high_resolution_clock::now()) {}

  ~ScopedTimer() {  // destructor
    auto t1 = std::chrono::high_resolution_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cout << label << " took " << ms << " ms\n";
    writeToCSV(label, ms);
  }
};

struct Task {
  std::string name;
  std::promise<std::string>
      prom;  // worker sets this (promise to set the value)
};

class GreeterServiceImpl final : public demo::Greeter::Service {
 public:
  GreeterServiceImpl() : stop_(false) {
    worker_ = std::thread([this] {
      // add logging to see when the worker starts and stops + debug
      std::cout << "[worker] Background worker started\n";
      for (;;) {
        Task dodo;
        {
          std::unique_lock<std::mutex> lock(
              m_);  // lock the mutex (wait for the condition variable to be signaled)
          cv_.wait(lock, [this] {
            return stop_ || !q_.empty();
          });  // wait for the condition variable (cv_) to be signaled - remember protected variables are named with a _
          if (stop_ && q_.empty()) {
            std::cout << "[worker] Background worker stopping\n";
            return;
          }
          dodo = std::move(q_.front());
          q_.pop();
        }

        std::cout << "[worker] Processing task for: " << dodo.name << "\n";
        {
          ScopedTimer t("worker task");
          std::this_thread::sleep_for(
              std::chrono::microseconds(100));  // 0.1ms work
          std::string output = "Hello, " + dodo.name + "!";
          dodo.prom.set_value(std::move(output));
        }
        std::cout << "[worker] Finished processing: " << dodo.name << "\n";
      }
    });
  }

  ~GreeterServiceImpl() override {  // destructor
    {
      std::lock_guard<std::mutex> lk(m_);
      stop_ = true;
    }
    cv_.notify_all();  // notify all waiting threads
    if (worker_.joinable()) worker_.join();
  }

  Status SayHello(ServerContext*, const demo::HelloRequest* req,
                  demo::HelloReply* rep) override {
    ScopedTimer timer("end-to-end RPC");

    {
      ScopedTimer direct_timer("direct processing");
      std::this_thread::sleep_for(
          std::chrono::microseconds(100));  // 0.1ms work
      std::string direct_result = "Hello, " + req->name() + "!";
    }

    // create a task + future
    Task dododo;
    dododo.name = req->name();
    auto fut = dododo.prom.get_future();

    // enqueue
    {
      std::lock_guard<std::mutex> lk(m_);
      q_.push(std::move(dododo));
      std::cout << "[server] Enqueued task for: " << req->name() << "\n";
    }
    cv_.notify_one();

    // wait for background worker to finish
    std::cout << "[server] Waiting for worker to process: " << req->name()
              << "\n";
    std::string out = fut.get();
    rep->set_message(std::move(out));
    std::cout << "[server] Response sent for: " << req->name() << "\n";
    return Status::OK;
  }

 private:
  std::mutex m_;
  std::condition_variable cv_;
  std::queue<Task> q_;
  std::thread worker_;
  bool stop_;  // flag to stop the background worker
};

int main() {
  GreeterServiceImpl welcome;  // service

  ServerBuilder bob_builder;
  bob_builder.AddListeningPort("0.0.0.0:50051",
                               grpc::InsecureServerCredentials());
  bob_builder.RegisterService(&welcome);

  std::unique_ptr<Server> server(bob_builder.BuildAndStart());
  std::cout << "Server running on 0.0.0.0:50051\n";
  server->Wait();
}
