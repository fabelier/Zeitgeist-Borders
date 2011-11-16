# -*- coding: utf-8 -*-

<%inherit file="layout.mako"/>
<form method="post" action="${request.route_url('home')}">
    Search : <input type="text" name="query" />
</form>
<div class="home">
% if result:
    <ul id="result">
        % for country in result:
            <li>
                ${country[0] | h}
                <ol>
                    % for line in country[1][1]:
                        <li>
                        ${line[0] | h}
                        </li>
                    % endfor
                </ol>
            </li>
        % endfor
    </ul>
%endif
</div>
