MsgCheck performs various checks on gettext files:

* compilation (with command `msgfmt -c`)
* for each translation:

  - number of lines in translated strings
  - whitespace at beginning/end of strings
  - trailing whitespace at end of lines inside strings
  - punctuation at end of strings
  - spelling (messages and translations).


