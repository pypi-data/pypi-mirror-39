import requests
import logging


def current_address():
	addr = requests.get("https://canihazip.com/s")
	logging.info(addr.content)
	return addr.content
