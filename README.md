# AvalonXmlAgent.bundle
[![Release](https://img.shields.io/github/release/joshuaavalon/AvalonXmlAgent.bundle/all.svg?style=flat-square&colorB=brightgreen)](https://github.com/joshuaavalon/AvalonXmlAgent.bundle/releases)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/joshuaavalon/AvalonXmlAgent.bundle/blob/master/LICENSE)

Avalon Xml Agent is a Plex TV and movie agent that is inspired by [XBMCnfoTVImporter.bundle](https://github.com/gboudreau/XBMCnfoTVImporter.bundle) and [XBMCnfoMoviesImporter.bundle](https://github.com/gboudreau/XBMCnfoMoviesImporter.bundle).
It is designed to use XML file as metadata instead of pull data from internet.
It allows you to maintain and backup your metadata much easier and prevent some random guys on internet modify the metadata that you used to.

See [Frequently Asked Questions](#frequently-asked-questions) for more details.

## Format
[See Wiki](https://github.com/joshuaavalon/AvalonXmlAgent.bundle/wiki/File-Format)

## Install
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

Then, select `Avalon XML TV Agent` and `Avalon XML Movie Agent` as your agent.

## Frequently Asked Questions

**Can XMBC nfo be used directly?**

No. Although XMBC and AvalonXml both use XML to store their data, XMBC allows many different tag to represent.
For example, `aired`, `premiered`, `dateadded` and `dayfirst` can represent the same information in XMBC.
AvalonXml only uses `aired`. It is not that difficult to write a script to read and write xml.

Also, although AvalonXml has legacy support for `.nfo`, it is recommend to use `.xml`. `.nfo` is not well support in 
many text editor. You have to manually select XML highlight.

**Why is this better than XMBC?**

* Cleaner code. For example, accessing the files on drive instead of query web API, etc.
* Consistent data. No more different tag name for same data. No unreasonable data (manually change duration instead of actual duration).
* Have [tool for generate XML file](https://github.com/joshuaavalon/AvalonXmlTools).
* Static naming. XMBC always search for `.nfo` with the same name of the video which cause problem when Plex choose between
multiple version video.

**Why some of the tags does not work?**

Those fields are exists in the code but Plex is not using it. I can do nothing about it.