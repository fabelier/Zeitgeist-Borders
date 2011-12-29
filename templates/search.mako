# -*- coding: utf-8 -*-

<%inherit file="layout.mako"/>
<div id="form" style="text-align: center">
    <form method="get" action="${request.route_url('search')}">
        <input type="text" name="q" value="${query | h}"/>
        <input type="submit" value="ok" />
    </form>
</div>
<div class="search">
% if result:
    <ul id="result">
        % for country, suggestions in result.iteritems():
            <li>
                ${countries[country] | h}
                <ol>
                    % for line in suggestions:
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

<image id="modelmap" src="/static/background.gif" width="100%"/>
<div id="map">
    <!--<div style="position:absolute;left:15%;top:35%;">USA</div>-->
</div>
