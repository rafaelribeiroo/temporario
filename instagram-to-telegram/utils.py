from socket import setdefaulttimeout, socket

# apt install -y speedtest-cli


# check if we have internet
def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        setdefaulttimeout(timeout)
        socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False
