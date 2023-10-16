# common-monday-supabase
[Lambda Layer](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/layers/common-monday-supabase/versions/13?tab=versions)

This is a custom layer that has a bunch of helper functions for supabase, monday.com, some types, and general helpers. This acts very similar to a python package through pypi. By doing this, you can share code easily between a bunch of different lambda functions.

`zip -r shared_code.zip ./python `

structure should be python/lib/file_names