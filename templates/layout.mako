# -*- coding: utf-8 -*-
<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>Zeitgeist Borders</title>
    <meta name="author" content="mandark">
    <link rel="shortcut icon" href="/static/favicon.ico">
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>
    % if request.session.peek_flash():
    <div id="flash">
        <% flash = request.session.pop_flash() %>
        % for message in flash:
        ${message}<br>
        % endfor
    </div>
    % endif

    <div id="menu">
        <a href="${request.route_url('home')}">HOME</a>
        <span class="separator"> - </span>
    </div>
    <div id="page">
        ${next.body()}
    </div>
    <div id="footer">
        Feel free to propose a new css :p
    </div>
    <script type="text/javascript">

      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-268798-8']);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>
</body>
</html>
