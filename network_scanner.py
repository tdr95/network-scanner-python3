import socket
import time
import collections
import functools
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Callable

class Protocol(Enum):
  HTTP = 1
  HTTPS = 2
  FTP = 3
  SSH = 4

Packet = collections.namedtuple("Packet", ["protocol", 'destination', 'data'])

def log_scan(func: Callable) -> Callable:
  @functools.wraps(func)
  def wrapper(scanner, *args, **kwargs):
    result = func(scanner, *args, **kwargs)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scan result: {result}")
    return result
  return wrapper

@dataclass
class ScanResult:
  protocol: Protocol
  destination: str
  status: str = field(default="UNKNOWN")
  response_time: float = field(default=0.0)

  def __str__(self):
    return (f"{self.__class__.__name__}(protocol={self.protocol.name}, destination={self.destination}, "
            f"status={self.status}, response_time={self.response_time:.2f}ms)")

  def __call__(self, *args: Any, **kwargs: Any) -> Any:
    return self.__str__()
  
  def __delattr__(self, item):
    object.__delattr__(self, item)
    print(f"Attribute {item} has been deleted")
  
  def __dir__(self):
    return super().__dir__()
  
  def __eq__(self, other):
    if isinstance(other, ScanResult):
      return (self.protocol == other.protocol and self.destination == other.destination 
              and self.status == other.status and self.response_time == other.response_time)
    return False
  
  def __format__(self, format_spec: str) -> str:
    return f"{self.__class__.__name__}[{self.protocol.name}, {self.destination}, {self.status}, {self.response_time:.2f}]"
  
  def __getstate__(self) -> object:
    return self.__dict__
  
  def __init_subclass__(cls) -> None:
    print(f"New subclass created: {cls.__name__}")

  def __ne__(self, other):
    return not self.__eq__(other)
    
  def __or__(self, other):
    if isinstance(other, ScanResult):
      return self.response_time or other.response_time
    return NotImplemented
  
  def __reduce__(self) -> str | tuple[Any, ...]:
    return (self.__class__, (self.protocol, self.destination, self.status, self.response_time))
  
  def __repr__(self) -> str:
    return (f"{self.__class__.__name__}(protocol={self.protocol.name}, destination={self.destination}, "
            f"status={self.status}, response_time={self.response_time:.2f}ms)")

  def __sizeof__(self) -> int:
    return super().__sizeof__()
  
  def __subclasses__(cls, C):
    if cls is ScanResult:
      if any("protocol" in B.__dict__ for B in C.__mro__):
        return True
    return NotImplemented
  
class NetworkScanner:
  def __init__(self, destination: str):
    self.destination = destination
  
  @log_scan
  def scan(self, protocol: Protocol) -> ScanResult:
    if protocol == Protocol.HTTP:
      return self._http_scan()
    elif protocol == Protocol.HTTPS:
      return self._https_scan()
    elif protocol == Protocol.FTP:
      return self._ftp_scan()
    elif protocol == Protocol.SSH:
      return self._ssh_scan()
    else:
      return ScanResult(protocol, self.destination, "UNSUPPORTED")
  
  def _http_scan(self) -> ScanResult:
    class _InternalHTTPScan:
      def __init__(self, destination):
        self.destination = destination
      
      def execute(self):
        start_time = time.time()
        try:
          with socket.create_connection((self.destination, 80), timeout=10) as sock:
            request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(self.destination)
            sock.sendall(request.encode())
            response = sock.recv(1024)
            status = "UP" if response else "DOWN"
        except socket.error:
          status = "DOWN"
        response_time = (time.time() - start_time) * 1000
        return ScanResult(Protocol.HTTP, self.destination, status, response_time)
    scanner = _InternalHTTPScan(self.destination)
    return scanner.execute()
 
  def _https_scan(self) -> ScanResult:
    class _InternalHTTPSScan:
      def __init__(self, destination):
        self.destination = destination
      
      def execute(self):
        start_time = time.time()
        try:
          with socket.create_connection((self.destination, 443), timeout=10) as sock:
            request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(self.destination)
            sock.sendall(request.encode())
            response = sock.recv(1024)
            status = "UP" if response else "DOWN"
        except socket.error:
          status = "DOWN"
        response_time = (time.time() - start_time) * 1000
        return ScanResult(Protocol.HTTPS, self.destination, status, response_time)
    scanner = _InternalHTTPSScan(self.destination)
    return scanner.execute()

  def _ftp_scan(self) -> ScanResult:
    class _InternalFTPScan:
      def __init__(self, destination):
        self.destination = destination
      
      def execute(self):
        start_time = time.time()
        try:
          with socket.create_connection((self.destination, 21), timeout=10) as sock:
            response = sock.recv(1024)
            status = "UP" if response else "DOWN"
        except socket.error:
          status = "DOWN"
        response_time = (time.time() - start_time) * 1000
        return ScanResult(Protocol.FTP, self.destination, status, response_time)
    scanner = _InternalFTPScan(self.destination)
    return scanner.execute()
  
  def _ssh_scan(self) -> ScanResult:
    class _InternalSSHScan:
      def __init__(self, destination):
        self.destination = destination
      
      def execute(self):
        start_time = time.time()
        try:
          with socket.create_connection((self.destination, 22), timeout=10) as sock:
            response = sock.recv(1024)
            status = "UP" if response else "DOWN"
        except socket.error:
          status = "DOWN"
        response_time = (time.time() - start_time) * 1000
        return ScanResult(Protocol.SSH, self.destination, status, response_time)
    scanner = _InternalSSHScan(self.destination)
    return scanner.execute()
