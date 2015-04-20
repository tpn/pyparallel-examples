def add_to_trie(trie, offset_trie, key, value):
    offset = int(value)
    if key in trie:
        existing = trie[key]
        if value not in existing:
            existing.append(offset)
            existing.sort()
    else:
        trie[key] = [ offset, ]

    if value in offset_trie:
        existing = offset_trie[value]
        if key not in existing:
            existing.append(key)
            existing.sort()
    else:
        offset_trie[value] = [ key, ]

    lower_value = key.lower()
    if lower_value == value:
        return

    if lower_value not in trie:
        trie[lower_value] = [ -offset, ]

scheme	0	URL scheme specifier	empty string
netloc	1	Network location part	empty string
path	2	Hierarchical path	empty string
params	3	Parameters for last path element	empty string
query	4	Query component	empty string
fragment	5	Fragment identifier	empty string
username	 	User name	None
password	 	Password	None
hostname	 	Host name (lower case)	None
port	 	Port number as integer, if present	None
