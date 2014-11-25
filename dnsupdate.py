#!/usr/bin/python
# easydns-updater.py ~ ajclarkson.co.uk
#
# Updater for Dynamic DNS on EasyDNS Domains
# Performs an update every 30 minutes for each given domain access token in
# the hosts.json file.

import json
from urllib2 import urlopen
import requests
import time

def get_cached_ip():
	'''
	Retrieve Cached IP From File, cuts down on API requests to EasyDNS if
	IP Address hasn't changed.

	Return: (string) Cached IP or 0 to force refresh of public IP
	'''
	try:
		cached_file = open('.easydns-cachedip', 'r')
		cached_ip = cached_file.read()
		cached_file.close()
		return cached_ip
	except IOError:
		return "0"

def set_cached_ip(ip):
	'''
	Stores IP Address in the Cached

	ip: (string) Address to be Cached
	'''
	try:
		cached_file = open('.easydns-cachedip', 'w')
		cached_file.write(ip)
		cached_file.close()
	except IOError, e:
		print e

def get_ip():
	'''
	Retrieves public IP (from httpbin) with cached IP and returns import

	Return: (string) Public IP
	'''
	public_ip = json.load(urlopen('http://httpbin.org/ip'))['origin']
	return public_ip

def load_hosts():
	'''
	Loads the hosts.json file containing access tokens for EasyDNS

	Return: (dict) Hosts and Access Tokens
	'''
	try:
		hosts_file = open('hosts.json', 'r')
		hosts_data = json.load(hosts_file)
		return hosts_data
	except IOError, e:
		print e

def update_host(token, current_ip):
	'''
	Formulate and Execute an Update request on EasyDNS API for a given access token / IP

	token: (string) Access Token for an EasyDNS Domain
	current_ip: (string) IP to point EasyDNS Domain to

	Return: Status (Either OK, or Error + Code)
	'''
	url = 'https://entrydns.net/records/modify/%s' % token
	payload = 'ip=%s' % current_ip
	response = requests.post(url, data=payload)
	if response.status_code == requests.codes.ok:
		return "OK"
	else:
		return "ERROR: Code %s" % response.status_code

'''
Forever Loop: Check Public IP against Cached IP, if different update specified
hosts before waiting 30 minutes and repeating.
'''
while True:
	current_ip = get_ip()
	cached_ip = get_cached_ip()
	if cached_ip != current_ip:
		hosts = load_hosts()
		for host in hosts:
			print "Updating %s: %s" % (host, update_host(hosts[host], current_ip))
	else:
		print "Public IP Matches Cache, Nothing to Do..."

	time.sleep(1800)



