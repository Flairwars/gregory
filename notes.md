Count command is run
<command> count
var:
    <str> color
    <class> ctx

runs <funct> get_stats
    var
        <str> colors
    runs <funct> get_color_database
        '''
        loads the json file with all the colors in
        replace with sql database
        '''
    runs <funct> get_posts
        '''
        reddit is loaded.
        color is gotten
        returns list of posts which contain name
        '''
    then loops though each page
    for each post on a page
        of author 

new code:
reddit folder:
    count.py
sql folder:
    count.py
commands folder:
    count.py

=-=-=-=-=-=-=-=-=-=-=-
command: code
=-=-=-=-=-=-=-=-=-=-=-

-[/] work out what sub it is referancing

-[/] get reddit posts of sub - use reddit/count.py
-[/] split posts into 25

function:
```py
loop though page

store known color of member raiding

try:
    get usercolor from dictionary
except KeyError:
    if unkown, make sql request to find user's color
    sql = 'select color from redditusers where username = %s'
    store in dictionary

return roygbp
```
yeild fuction
