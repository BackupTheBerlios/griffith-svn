## -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
    <head>
        ${self.head_tags()}
    </head>
    <body>
        <h1>${ self.header() }</h1>
        ${ self.body() }
        ${ self.footer() }
    </body>
</html>

<%def name="header()">
    ${c.header}
</%def>
<%def name="footer()">
<div id="footer"><small>Pylons &amp; WebGriffith powered</small></div>
</%def>
<%def name="head_tags()">
    <title>WebGriffith</title>
</%def>
