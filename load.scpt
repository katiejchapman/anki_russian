set searchTerm to the clipboard as text
set openRussianURL to "https://en.openrussian.org/ru/" & searchTerm
set wiktionaryURL to "https://en.wiktionary.org/wiki/" & searchTerm & "#Russian"
set forvoURL to "https://forvo.com/search/" & searchTerm & "/ru/"
set ruWiktionaryURL to "https://ru.wiktionary.org/wiki/" & searchTerm

tell application "Safari" to activate

-- load word definitions
tell application "Safari"
   activate
   set i to 0
   set tabList to every tab of window 1
   set tabCount to count of tabList
   repeat tabCount times
      tell window 1
         set i to i + 1
         set textURL to (URL of tab i) as text
         -- load the word in open russian
         if textURL begins with "https://en.openrussian.org" then
            set encodedURL to urlEncode(openRussianURL) of me
            
            set URL of tab i to encodedURL
            
         end if
         -- load the word in wiktionary
         if textURL begins with "https://en.wiktionary.org" then
            set URL of tab i to urlEncode(wiktionaryURL) of me
            -- make the wiktionary tab the active tab
            try
               set current tab of window 1 to tab i
            end try
            
         end if
         
         if textURL begins with "https://forvo.com" then
            set URL of tab i to urlEncode(forvoURL) of me
         end if
         
         if textURL begins with "https://ru.wiktionary.org" then
            set URL of tab i to urlEncode(ruWiktionaryURL) of me
         end if
      end tell
   end repeat
end tell

-- encode Cyrillic test as "%D0" type strings
on urlEncode(input)
   tell current application's NSString to set rawUrl to stringWithString_(input)
   set theEncodedURL to rawUrl's stringByAddingPercentEscapesUsingEncoding:4 -- 4 is NSUTF8StringEncoding
   return theEncodedURL as Unicode text
end urlEncode