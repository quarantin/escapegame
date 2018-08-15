
# Generic JSON import functions

def generic_json_import(model, dic):

	try:
		try:
			obj = model.objects.get(id=dic['id'])
			for key, val in dic.items():
				setattr(obj, key, val)
		except:
			obj = model(**dic)

		obj.save()

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s<br>\n%s' % (err, traceback.format_exc().replace('\n', '<br>\n'))

def generic_json_import_list(model, listdic):

	try:
		for dic in listdic:
			status, message = generic_json_import(model, dic)
			if status != 0:
				return status, message

		return 0, 'Success'

	except Exception as err:
		return 1, 'Error: %s' % err

