$rss = Invoke-WebRequest -Uri 'https://feeds.bbci.co.uk/news/world/rss.xml' -UseBasicParsing | Select -Expand Content
[xml]$xml = $rss
$xml.rss.channel.item | Select -First 15 | Select -Expand Title
