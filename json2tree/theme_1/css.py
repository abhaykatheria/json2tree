css = '''
<style>
ul, #myUL {
    list-style-type: none;
}
li {
    padding-top: 5px;padding-bottom: 5px;
}
#myUL {
    margin: 0;
    padding: 0;
}
.caret {
    cursor: pointer;
    user-select: none;
    font-family: 'Inconsolata', monospace;
}
.caret::before {
    content: " \\25B6";
    display: inline-block;
margin-right: 6px;
}
.caret-down::before {
    transform: rotate(90deg); 
}
.nested {
    display: none;
}
.active {
    display: block;
}
.header {
    text-align: left;
    background: #f1f1f1;
}
.text-c {
    color:green;
    font-family:'Inconsolata',monospace;
}
.text-h {
    font-family:'Inconsolata',monospace;
}
</style>\n
'''
