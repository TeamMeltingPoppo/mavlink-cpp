# mavlink-cpp

Generated C++ library for the avionics system's custom MAVLink dialect.

This repository provides the C++ library generated from [`mavlink-dialect`](../mavlink-dialect). It is intended to be used by firmware and other C++ applications that communicate using the project's MAVLink message definitions.

## Usage

Add `mavlink-cpp` as a dependency of your firmware or C++ application and use the generated MAVLink types and serialization/deserialization functions.

The generated code should not be modified manually.

## Development

The library is generated from `mavlink-dialect`. Changes to message definitions should be made in the dialect repository rather than directly in this repository.

See the repository's development documentation for the generation and release process.

## Related Repositories

* `mavlink-dialect` — MAVLink message definitions
* `mavlink-canfd` — CAN FD transport
