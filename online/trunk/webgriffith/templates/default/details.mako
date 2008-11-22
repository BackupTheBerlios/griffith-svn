## -*- coding: utf-8 -*-
<%page args="movie, **kwargs"/>

##            'cameraman'      : _('Cameraman'),
##            'color'          : _('Color'),
##            'cond'           : _('Condition'),
##            'image'          : _('Image'),
##            'layers'         : _('Layers'),
##            'media_num'      : _('Discs'),
##            'ratio_id'       : _('Aspect ratio'),
##            'region'         : _('Region'),
##            'screenplay'     : _('Screenplay'),
##            'vcodec_id'      : _('Video codec'),

<table id="m_${movie.number}">
 
	<tr class="title">
		<th>${_('Title')}</th>
		<td>${movie.title}</td>
	</tr>
	<tr class="o_title">
		<th>${_('Original title')}</th>
		<td>${movie.o_title}</td>
	</tr>
	<tr class="number">		
		<th>${_('Number')}</th>
		<td>${movie.number}</td>
	</tr>
	<tr class="year">
		<th>${_('Year')}</th>
		<td>${movie.year}</td>
	</tr>
	<tr class="director">
		<th>${_('Director')}</th>
		<td>${movie.director}</td>
	</tr>
	<tr class="rating">
		<th>${_('Rating')}</th>
		<td>${movie.rating}</td>
	</tr>
	<tr class="runtime">
		<th>${_('Runtime')}</th>
		<td>${movie.runtime}</td>
	</tr>
	<tr class="country">
		<th>${_('Country')}</th>
		<td>${movie.country}</td>
	</tr>
	<tr class="genre">
		<th>${_('Genre')}</th>
		<td>${movie.genre}</td>
	</tr>
% if movie.o_site:
	<tr class="links">
		<th>${_('Official site')}</th>
		<td><a href="${movie.o_site}">${movie.o_site}</a></td>
	</tr>
% endif
% if movie.site:
	<tr class="links">
		<th>${_('Site')}</th>
		<td><a href="${movie.site}">${movie.site}</a></td>
	</tr>
% endif
% if movie.trailer:
	<tr class="links">
		<th>${_('Trailer')}</th>
		<td><a href="${movie.trailer}">${movie.trailer}</a></td>
	</tr>
% endif
	<tr class="media">
		<th>${_('Medium')}</th>
		<td>${movie.medium.name}</td>
	</tr>
% if movie.collection:
	<tr class="collection">
		<th>${_('Collection')}</th>
		<td>${movie.collection.name}</td>
	</tr>
% endif
% if movie.volume:
	<tr class="volume">
		<th>${_('Volume')}</th>
		<td>${movie.volume.name}</td>
	</tr>
% endif
	<tr class="seen">
		<th>${_('Seen it')}</th>
        <td>
% if movie.seen:
		${_('Yes')}
% else:
		${_('No')}
% endif
        </td>
	</tr>
	<tr class="loaned">
		<th>${_('Loaned')}</th>
        <td>
% if movie.loaned:
		${_('Yes')}
% else:
		${_('No')}
% endif
        </td>
	</tr>
	<tr class="classification">
		<th>${_('Classification')}</th>
		<td>${movie.classification}</td>
	</tr>
	<tr class="studio">
		<th>${_('Studio')}</th>
		<td>${movie.studio}</td>
	</tr>
	<tr class="cast">
		<th>${_('Cast')}</th>
		<td>${movie.cast}</td>
	</tr>
	<tr class="plot">
		<th>${_('Plot')}</th>
		<td>${movie.plot}</td>
	</tr>
	<tr class="notes">
		<th>${_('Notes')}</th>
		<td>${movie.notes}</td>
	</tr>
</table>
