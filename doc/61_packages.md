### Packages

Sometimes you will want to use code from 
external API's or packages.

The package manager is very incomplete, 
and has room for much improvement. However, 
certain packages can be installed without the
use of PCPM.

Let's get started by showing how to install
FileEssentials.

Start by by running this:

```shell
rm FileEssentials/* .
rm FileEssentials/.* .
rmdir FileEssentials

wget "http://github.com/DaRubyMiner360/FileEssentials/archive/ParaCode-Rewrite.zip" -O temp.zip
unzip temp.zip
rm temp.zip

mv FileEssentials-ParaCode-Rewrite/* .
mv FileEssentials-ParaCode-Rewrite/.* .
```

Now, read through the FileEssentials README.