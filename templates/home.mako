# -*- coding: utf-8 -*-

<%inherit file="layout.mako"/>
<form method="post" action="${request.route_url('home')}">
    <input type="text" name="query" />
    <input type="submit" value="ok" />
</form>
<div class="home">
% if result:
    <ul id="result">
        % for country in result:
            <li>
                ${country[0] | h}
                <ol>
                    % for line in country[1]:
                        <li>
                        ${line | h}
                        </li>
                    % endfor
                </ol>
            </li>
        % endfor
    </ul>
%endif
</div>

<image id="modelmap" src="static/background.gif" width="100%"/>
<div id="map">
    <div style="position:absolute;left:15%;top:35%;">USA</div>
</div>
