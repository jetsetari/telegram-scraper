"""
SEND MESSAGE
"""
import os

#CONFIG
from config.globals import lg, n, r, w, cy, ye
from config.header import banner

while True:
	os.system('clear')
	banner()
	print(w+'=== SEND MESSAGE'+n)
	input('\nIn development... Press enter to go back to main menu')
	break


	# c(functions.users.GetFullUserRequest(id=user_id))

    # def send_message_to_user(user_id, message):
    #     try:
    #         # Use InputPeerUser directly, no need to call get_input_entity.
    #         user_peer = InputPeerUser(user_id, 0)  # Replace 0 with the actual access_hash if available.
    #         c.send_message(user_peer, message)
    #     except Exception as e:
    #         print(f"Error: {e}")
    # send_message_to_user(user_id, "hi")
    #print(test_user)
    #c.send_message(InputPeerUser(test_user.user_id, test_user.access_hash), "hi")