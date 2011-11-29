# -*- coding: utf-8 -*-

<%inherit file="layout.mako"/>
<div id="form" style="text-align:center">
    <form method="get" action="${request.route_url('search')}">
        <input type="text" name="q" />
        <input type="submit" value="ok" />
    </form>
</div>
<div style="text-align:center;">
<div style="display:block;width:350px;font-family:verdana,sans-serif;margin-left:auto;margin-right:auto;text-align:justify;font-size:12px;">
<p>
Zeitgeist Borders aims at providing a visualization of every country specific Google Search services. Type a query, you'll see what each country get as recommendation.<br />
<p>
For example, For the query 'test' google recommends to some country 'love' and for others 'testicular cancer'.<br />
<p>

</div>
<a href="http://wiki.fabelier.org/index.php?title=Zeitgeist_Borders" style="text-decoration:none;font-size=90%;text-align:right" target="_blank">more...</a>
</div>

