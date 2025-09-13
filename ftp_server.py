from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Base directory to serve files from
BASE_DIR = r"E:\web-server"

def main():
    # Create a user manager
    authorizer = DummyAuthorizer()

    # Add a user "user" with password "12345"
    # Change these to whatever you want
    authorizer.add_user("user", "12345", BASE_DIR, perm="elradfmwMT")

    # Add anonymous login (read-only)
    # comment this out if you don’t want anonymous
    authorizer.add_anonymous(BASE_DIR)

    # Set up FTP handler
    handler = FTPHandler
    handler.authorizer = authorizer

    # Bind server to your local IP and port 2121
    server = FTPServer(("192.168.8.19", 2121), handler)

    print(f"FTP server running at ftp://192.168.8.19:2121/ serving {BASE_DIR}")
    server.serve_forever()

if __name__ == "__main__":
    main()
