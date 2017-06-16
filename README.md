# AvalonXmlAgent.bundle
[![Release](https://img.shields.io/github/release/joshuaavalon/AvalonXmlAgent.bundle/all.svg?style=flat-square&colorB=brightgreen)](https://github.com/joshuaavalon/AvalonXmlAgent.bundle/releases)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/joshuaavalon/AvalonXmlAgent.bundle/blob/master/LICENSE)

Avalon Xml Agent is a Plex TV and movie ageet that is inspired by [XBMCnfoTVImporter.bundle](https://github.com/gboudreau/XBMCnfoTVImporter.bundle) and [XBMCnfoMoviesImporter.bundle](https://github.com/gboudreau/XBMCnfoMoviesImporter.bundle).
It is designed to use XML file as metadata instead of pull data from internet.
It allows you to maintain and backup your metadata much easier and prevent some random guys on internet modifiy the metadata that you used to.

## Compare to XBMCnfoTVImporter and XBMCnfoTVImporter
Avalon Xml Agent is very strict about naming convention and nfo format. This allows much cleaner code. Also, Avalon Xml Agent has the mininal feature.

One of the feature is static nfo name. It can read `show - s01e01.nfo` even when a better version `show - s01e01.hd.mp4` has been add.

## Compbability
> XBMCnfoTVImporter, XBMCnfoMoviesImporter > AvalonXmlAgent

Only specific tags are working.

> AvalonXmlAgent > XBMCnfoTVImporter, XBMCnfoMoviesImporter

It should work expect for `director`, `writer` and multiple `set`

## Format
[See Wiki](https://github.com/joshuaavalon/AvalonXmlAgent.bundle/wiki/File-Format)

## Install
The following assume you use Ubuntu

### Git
```sh
cd /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/
sudo git clone https://github.com/joshuaavalon/AvalonXmlAgent.bundle.git
sudo chown plex:plex AvalonXmlAgent.bundle
sudo service plexmediaserver restart
```

### Maually
```sh
sudo wget https://github.com/joshuaavalon/AvalonXmlAgent.bundle/archive/master.zip -P /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/
sudo unzip master.zip -d AvalonXmlAgent.bundle
sudo chown plex:plex AvalonXmlAgent.bundle
sudo service plexmediaserver restart
```
