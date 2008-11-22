## -*- coding: utf-8 -*-
## vim: ft=mako
<%inherit file="base.mako"/>

<div class="settings">
    <p>${_('Language')}: ${c.session['lang']}</p>
    <p>${_('Template')}: ${c.session['template']}</p>
    <p>${_('Items per page')}: ${c.session['items_per_page']}
        <a href="${ h.url_for(controller='settings', action='set', items=c.session['items_per_page']-1) }">-</a>
        <a href="${ h.url_for(controller='settings', action='set', items=c.session['items_per_page']+1) }">+</a>
</p>
</div>
<p>
    <a href="${ h.url_for(controller='', action=None, id=None) }">main page</a>
</p>
