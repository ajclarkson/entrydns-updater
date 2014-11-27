# EntryDNS Updater

A basic python script to update EntryDNS A Records providing dynamic DNS on a custom domain.

## Requirements

1) EntryDNS must be the name server for your domain (`ns1.entrydns.com`, `ns2.entrydns.com`)

2) You must create an A record for the domain within EntryDNS, which will grant you with an API token for updating that domain.

## Updating Hosts

The entrydns-updater script can update as many hosts as you would like to your current public IP address. In order to configure the script, see the `example.hosts.json` file for the expected format. This file should be created/renamed as `hosts.json`.

The `reference-id` is purely for your reference and will be used in log scripts, so choose a sensible unique name relating to your domain/host. The `entrydns-access-token` is the API token generated when creating an A record for the domain.

Running the script will read your current IP address and check it against a cache file, this is to prevent you spamming EntryDNS with update requests if no update is needed. The cache file is automatically created and resides within the entrydns-updater directory as `.entrydns-cachedip`.

When your public IP does not match this cache, an update request will be performed for each entry within the `hosts.json` file.

## Automating the task

The script has been engineered to be a run once update solution at the moment, and as such it is a perfect candidate for `cron`:

```
30	*	*	*	* /path/to/entrydns-updater/entrydns-updater.py
```

That would be a good starting point for running every 30 minutes.