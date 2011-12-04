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
	  if not dojo.attr(elem, 'value')
		  select.store.fetch
			  onComplete: (items) ->
				  if items.length < 1
					  value = ''
				  else
					  value = select.store.getIdentity(items[0])
				  select.setValue(value)
	  else
		  select.setValue(dojo.attr(elem, 'value'))
	  if dojo.hasAttr(elem, 'data-parent')
		  parent = dijit.byId(dojo.attr(elem, 'data-parent'))
		  child = select
		  dojo.connect parent, 'onChange', parent, (evt) ->
			  dojo.attr(child, 'query',
				  parent: this.value)
			  child.store.fetch
				  query:
					  parent: this.value
				  onComplete: (items) ->
					  if items.length < 1
						  value = ''
					  else
						  value = child.store.getIdentity(items[0])
					  child.setValue(value)

make_form = (elem) ->
	args =
		method: dojo.attr(elem, 'method') || ''
		action: dojo.attr(elem, 'action') || ''
		enctype: dojo.attr(elem, 'enctype')
	form = new dijit.form.Form(args, elem)
	form.onSubmit = (evt) ->
		return this.validate()

decorate_input = (li, store) ->
	input = dojo.query('input', li)[0]
	input.id = null
	select = new dijit.form.ComboBox(
		store: store
		searchAttr: 'label'
		name: dojo.attr(input, 'name')
		value: dojo.attr(input, 'value'),
	input)
	remove_input = (evt) ->
		select.destroy()
		dojo.destroy(li)
		dojo.destroy(remove_button)
	remove_button = dojo.create('span',
		"class": "removeButton"
		innerHTML: "X"
		title: "supprimer",
		select.domNode, 'after')
	dojo.connect(remove_button, 'onclick', remove_button, remove_input)
	return select

make_array_input = (section) ->
	elem = dojo.query('li', section)[0]
	input_template = '<li>' + dojo.attr(elem, 'innerHTML') + '</li>'
	input = dojo.query('li input', section)[0]
	base_url = dojo.attr(input, 'data-datastore-url')
	full_url = base_url
	if dojo.attr(input, 'data-basefilter')
		filter = dojo.query('input[id=base_filter]')[0]
		filter = dojo.attr(filter, 'value')
		full_url = base_url + '?' + filter
		base_select = dijit.byId(dojo.attr(input, 'data-basefilter'))
	store = new dojo.data.ItemFileReadStore
			url: full_url
			clearOnClose: true
	if base_select
		make_change = (store, base_url) =>
			return (newvalue) => 
				store.url = base_url + '?' + filter.split('=')[0] + '=' + newvalue
				store.close()
		dojo.connect base_select, 'onChange', make_change(store, base_url)
	decorate_input(li, store) for li in dojo.query('li', section)
	add_input = (evt) ->
		container = dojo.place(input_template, section, 'last')
		input = dojo.query('input', container)[0]
		select = decorate_input(container, store)
		select.setValue('')
		dojo.place(section.add_button.domNode, section, 'last')
		select.focus()
	add_button = new dijit.form.Button
		onClick: add_input
		label: "Ajouter"
		"class": "addButton"
		id: 	 "add_input_#{ input.name }"
	section.add_button = add_button
	dojo.place(add_button.domNode, section, 'last')
		  

dojo.addOnLoad () =>
	make_select elem for elem in dojo.query('input[data-treeselect]')
	make_form(form) for form in dojo.query('form[data-form]')
	make_array_input(section) for section in dojo.query('ul[data-islist]')
