cmake_minimum_required(VERSION 3.15)
project(GrpcHello CXX)
set(CMAKE_CXX_STANDARD 17)

# Find gRPC, which will also find Protobuf
find_package(gRPC CONFIG REQUIRED)

set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR})
set(PROTO_SRC ${GEN_DIR}/inference.pb.cc)
set(GRPC_SRC ${GEN_DIR}/inference.grpc.pb.cc)

add_custom_command(
  OUTPUT ${PROTO_SRC} ${GRPC_SRC}
  COMMAND $<TARGET_FILE:protobuf::protoc>
          --proto_path=${CMAKE_CURRENT_SOURCE_DIR}
          --cpp_out=${GEN_DIR}
          --grpc_out=${GEN_DIR}
          --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>
          ${CMAKE_CURRENT_SOURCE_DIR}/inference.proto
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/inference.proto
  DEPENDS protobuf::protoc
  DEPENDS gRPC::grpc_cpp_plugin
)

add_executable(server main.cpp ${PROTO_SRC} ${GRPC_SRC})
target_include_directories(server PRIVATE ${GEN_DIR})
target_link_libraries(server PRIVATE gRPC::grpc++ protobuf::libprotobuf)

add_executable(client client.cpp ${PROTO_SRC} ${GRPC_SRC})
target_include_directories(client PRIVATE ${GEN_DIR})
target_link_libraries(client PRIVATE gRPC::grpc++ protobuf::libprotobuf)
