make_select = (elem) ->
	store = new dojo.data.ItemFileReadStore(
		url: dojo.attr(elem, 'data-datastore-url')
	)
	args =
		id: elem.id
		name: elem.name
		value: dojo.attr(elem, 'value')
		placeholder: 'Choisir...'
		store: store
		autocomplete: true
		searchAttr: "label"
	select = new dijit.form.FilteringSelect(args, elem)
	select.message = 'Choisir...'
	if dojo.hasAttr(elem, 'data-parent')
	  parent = dijit.byId(dojo.attr(elem, 'data-parent'))
	  dojo.connect parent, 'onChange', parent, (evt) ->
		  select.query =
			  parent: this.value
		  select.store.fetch
			  query:
				  parent: this.value
			  onComplete: (items) ->
				  if items.length < 1
					  value = ''
				  else
					  value = select.store.getIdentity(items[0])
				  select.setValue(value)
	else
	  select.store.fetch
		  onComplete: (items) ->
			  if items.length < 1
				  value = ''
			  else
				  value = select.store.getIdentity(items[0])
			  select.setValue(value)

make_form = (elem) ->
	args =
		method: dojo.attr(elem, 'method')
		action: dojo.attr(elem, 'action')
		enctype: dojo.attr(elem, 'enctype')
	form = new dijit.form.Form(args, elem)
	form.onSubmit = (evt) ->
		return this.validate()

dojo.addOnLoad () =>
	make_select(elem) for elem in dojo.query('input[data-datastore-url]')
	make_form(form) for form in dojo.query('form')
