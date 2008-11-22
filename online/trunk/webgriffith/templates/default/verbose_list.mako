## -*- coding: utf-8 -*-
## vim: ft=mako
<%inherit file="base.mako"/>
<%namespace name="details_tpl" file="details.mako"/>

<div id="movie_list">
     ${showpage(movies)}
</div>

<p>
    <a href="${ h.url_for(action='page', id=movies.page) }">normal mode</a>
</p>

<%def name="showpage(movies)">
    <p class="movie_list_pagenum">
        ${movies.pager('$link_previous $page/$last_page $link_next', page_param='id', onclick="$('#movie_list').load('%s'); return false")}
    </p>
    % for movie in movies:
        ${details_tpl.body(movie=movie)}
        <hr />
    % endfor
    <p>
        ${ movies.pager('~5~', page_param='id', onclick="$('#movie_list').load('%s'); return false") }
    </p>
</%def>

## include jQuery (for pagination)
<%def name="head_tags()">
    ${parent.head_tags()}
    ${h.javascript_link('/js/jquery.min.js')}
</%def>
