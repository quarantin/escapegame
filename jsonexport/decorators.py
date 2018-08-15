"""
	Implement decorator `json_import`
"""
def json_import(model):

	def json_import (self, dic):

		try:
			try:
				obj = self.model.objects.get(id=dic['id'])
				for key, val in dic.items():
					setattr(obj, key, val)
			except:
				obj = self.model(**dic)

			obj.save()

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s<br>\n%s' % err

	def json_import_list(self, listdic):

		try:
			for dic in listdic:
				status, message = self.json_import(dic)
				if status != 0:
					return status, message

			return 0, 'Success'

		except Exception as err:
			return 1, 'Error: %s' % err

	model.json_import = json_import
	model.json_import_list = json_import_list

	return model
