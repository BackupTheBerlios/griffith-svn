## -*- coding: utf-8 -*-
## vim: ft=mako
<%inherit file="base.mako"/>

<div id="movie_list">
     ${showpage(movies)}
</div>

<p class="settings">
    <a href="${ h.url_for(action='verbose', id=movies.page) }">verbose mode</a>
    <a href="${ h.url_for(controller='settings', action=None, id=None) }">settings</a>
</p>

<hr/> 


<%def name="showpage(movies)">
    <p class="movie_list_pagenum">
        ${movies.pager('$link_previous $page/$last_page $link_next', page_param='id', onclick="$('#movie_list').load('%s'); return false")}
    </p>
    % for movie in movies:
    <div class="movie_list_row">
        <span class="movie_list_number">${movie.number}</span>
        <span class="movie_list_title">
            <a href="${ h.url_for(controller='movie', action='view', id=movie.number) }">${movie.title}</a>
        </span>
    </div>
    <hr />
    % endfor
    <p>
        ${ movies.pager('~5~', page_param='id', onclick="$('#movie_list').load('%s'); return false") }
    </p>
</%def>

<%def name="head_tags()">
    ${parent.head_tags()}
    ${h.javascript_link('/js/jquery.min.js')}
</%def>
