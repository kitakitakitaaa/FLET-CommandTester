from pythonosc import udp_client

ip = "127.0.0.1"
port = 7000

client = udp_client.SimpleUDPClient(ip, port)  # Create client

client.send_message("/some/address", 123)   # Send float message
client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string