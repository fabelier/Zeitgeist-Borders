# -*- coding: utf-8 -*-

<%inherit file="layout.mako"/>
<div id="form" style="text-align: center">
    <form method="get" action="${request.route_url('search')}">
        <input type="text" name="q" />
        <input type="submit" value="ok" />
    </form>
</div>
